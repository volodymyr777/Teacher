# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db import IntegrityError
from .models import DataR, DataJ, Tema, Rozklad, Uch, Journal
import xlrd
import sqlite3
from django.conf import settings
from datetime import datetime, date, timedelta
import datetime
from .forms import TemaForm, RozkladForm, UploadFileForm

from cont_proc import str_to_int
from cont_switch import switch_case

def repoze(request):
    if request.method == "POST":
        try:
            new_date = request.POST['add_date']
            DataR.objects.create(
                dat=datetime.datetime.strptime(new_date, '%d-%m-%Y')
            )
        except (ValueError, IntegrityError):
            ct= DataR.objects.all()
            ctt = []
            max_id = 1
            for el in ct:
                if el.id > max_id:
                    max_id = el.id
            for i, el in enumerate(range(max_id)):
                rez = request.POST.get('mitka'+str(i+1))
                if rez == 'on':
                    ctt.append(i+1)
                else:
                    ctt.append(0)
            for i in ctt:
                DataR.objects.filter(id=i).delete()
            pass

    ctx = {
        'dat' : DataR.objects.all()
    }
    return render(request, 'repoze.html', ctx)

def job(request):
    if request.method == "POST":
        new_den = request.POST['add_den']
        if str(new_den) != 'виберіть день':
            nom_den = switch_case(new_den)
            new_date = request.POST['add_date']
            DataJ.objects.create(
                dat=datetime.datetime.strptime(new_date, '%d-%m-%Y'),
                num = nom_den,
                name = new_den
            )
        else:
            ct= DataJ.objects.all()
            ctt = []
            max_id = 1
            for el in ct:
                if el.id > max_id:
                    max_id = el.id
            for i, el in enumerate(range(max_id)):
                rez = request.POST.get('mitka'+str(i+1))
                if rez == 'on':
                    ctt.append(i+1)
                else:
                    ctt.append(0)
            for i in ctt:
                DataJ.objects.filter(id=i).delete()
            pass

    ctx = {
        'dat' : DataJ.objects.all()
    }
    return render(request, 'job.html', ctx)

def rozklad(request):
    if request.method == "POST":
        new_den = request.POST['add_den']
        if str(new_den) != 'виберіть день':
            nom_den = switch_case(new_den)
            Rozklad.objects.create(
                num = nom_den,
                name = new_den
            )
        else:
            ct= Rozklad.objects.all()
            ctt = []
            max_id = 1
            for el in ct:
                if el.id > max_id:
                    max_id = el.id
            for i, el in enumerate(range(max_id)):
                rez = request.POST.get('mitka'+str(i+1))
                if rez == 'on':
                    ctt.append(i+1)
                else:
                    ctt.append(0)
            for i in ctt:
                Rozklad.objects.filter(id=i).delete()
            pass

    ctx = {
        'dni' : Rozklad.objects.all()
    }
    return render(request, 'rozklad.html', ctx)

def tema(request):
    form = UploadFileForm(request.POST, request.FILES)
    #form = TemaForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        try:
            vybir_kn = request.POST.get('itema')
            # вибрали кнопку "Імпортувати теми з Excel"
            if vybir_kn== 'item':
                file_source = str(request.FILES.get(r'file'))
                try:
                    # вміст таблиці Tema видаляємо лише тоді, коли вибрали файл для завантаження
                    if file_source != 'None':
                        Tema.objects.all().delete()
                    rb = xlrd.open_workbook(file_source, formatting_info=True)
                    sheet = rb.sheet_by_index(0)
                    for rownum in range(sheet.nrows):
                        row = sheet.row_values(rownum)
                        Tema.objects.create(
                            num = str(str_to_int(row[0])),
                            tema = row[1]
                        )
                except:
                    pass

            # вибрали кнопку "Імпортувати розрахункові дати"
            # повний шлях до бази даних
            db_path =settings.DATABASES['default']['NAME']
            if vybir_kn == 'iden':
                # перевірка на вірність вибору кнопки print(vybir_kn)
                # робота з додатковими вихідними
                rep_data = DataR.objects.all()
                r = []
                for i in rep_data:
                    r.append(i.dat)

                # робота з додатковими робочими
                job_data = DataJ.objects.all()
                jdat = []
                jnum = []
                for i in job_data:
                    jdat.append(i.dat)
                    jnum.append(i.num)

                # робота з Розкладом
                roz_num = Rozklad.objects.all()
                roz = []
                for i in roz_num:
                    roz.append(i.num)

                today = date.today()
                rik = today.year
                mis = today.month
                # якщо текучий місяць в діапазоні з 6 по 12,
                # то навчальний рік вважається текучим роком
                # інакше навчальний рік зменшуємо на 1,
                # оскільки ми в текучому навчальному році
                if mis>=1 and mis <=5:
                    rik = rik -1
                dtp = date(rik,9,1)
                dtk = date(rik+1,5,31)
                dt = dtp-timedelta(days=1)
                # обхід всього діапазону ы формування списку робочих дат
                rdat = []
                while dt<=dtk:
                    dt = dt+timedelta(days=1)
                    # якщо дата не входить у масив додаткових вихідних
                    if dt not in r:
                        # якщо дата входить у період робочих днів:
                        # (понеділок - п'ятниця) то відбираємо,
                        # та перевіряємо в розкладі на цей день уроку
                        if dt.weekday()<5:
                            for el_rozklad in roz:
                                if el_rozklad == dt.weekday():
                                    rdat.append(dt)
                        # інакше, дивимось чи дата входить у додаткові робочі
                        # якщо входить, то відбираємо
                        # та перевіряємо в розкладі на цей день уроку
                        else:
                            for el in range(len(jdat)):
                                if dt == jdat[el]:
                                    for el_rozklad in roz:
                                        if el_rozklad == jnum[el]:
                                            rdat.append(dt)
                # сформовано список rdat робочих дат викладання предмету
                #for l in rdat:
                    #print(l)


                # Обновлення поля dat таблиці Tema
                inf_tema = Tema.objects.all()

                # визначаємо id вибраного елемента таблиці vyb
                ctt = []
                max_id = 1
                for el in inf_tema:
                    if el.id > max_id:
                        max_id = el.id
                for i, el in enumerate(range(max_id)):
                    rez = request.POST.get('mitka'+str(i+1))
                    if rez == 'on':
                        ctt.append(i+1)
                    else:
                        ctt.append(0)
                #print(max(ctt))
                vyb = max(ctt)


                j = 0
                for inf in inf_tema:
                    # якщо не заголовчний рядок
                    if inf.num != '':
                        # якщо зроблено вибір
                        if vyb > 0:
                            d = Tema.objects.get(id=vyb)
                            # шукаємо дату фіксації вибору d.dat
                            #print(d.dat, inf.dat)
                            # робимо зміну поля дати для всіх значень, дата яких більша вибраної дати
                            if inf.dat > d.dat:
                                #print(rdat[j])
                                tem = Tema.objects.get(dat=inf.dat)
                                tem.dat = rdat[j]
                                tem.save()
                        else:
                            # якщо не зроблено вибору, vyb ==0, то обновляємо поле дада по всіхрядках таблиці
                            tem = Tema.objects.get(id=inf.id)
                            tem.dat = rdat[j]
                            tem.save()
                        j = j + 1

        except:
            pass
    ctx = {
        'form' : form,
        'elements' : Tema.objects.all()
    }

    if form.is_valid():
        form.save()

    return render(request, 'tema.html', ctx)

def uchni(request):
    if request.method == "POST":
        try:
            new_uch = request.POST['add_uch']
            Uch.objects.create(
                pib = new_uch
            )
        except:
            pass

    ctx = {
        'uchni' : Uch.objects.all()
    }
    return render(request, 'uchni.html', ctx)

def journal(request):
    ctx = {
        'dat' : Tema.objects.all(),
        'pib' : Uch.objects.all(),
        'jor' : Journal.objects.all()
    }
    return render(request, 'journal.html', ctx)

def journal_edit(request):
    if request.method == "POST":
        try:
            td = Tema.objects.all()
            uc = Uch.objects.all()
            for uu in uc:
                for dd in td:
                    if dd.num !='':
                        u = uu.id
                        d = dd.num
                        edit = request.POST.get('oc-'+str(uu.id)+'-'+str(dd.num))
                        try:
                            j = Journal.objects.get(tema_id=d , uch_id=u)
                            #j = Journal.objects.filter(uch_id=u).get(tema_id=d)
                            j.ocinka = edit
                            j.save()
                        except Journal.DoesNotExist:
                            Journal.objects.create(
                                uch_id = u,
                                tema_id = d,
                                ocinka = edit
                            )
                        #print(u, d, edit)

        except:
            pass
    ctx = {
        'dat' : Tema.objects.all(),
        'pib' : Uch.objects.all(),
        'jor' : Journal.objects.all()
    }
    return render(request, 'journal_edit.html', ctx)