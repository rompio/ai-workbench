from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Aktivitäten, AktivitätenUser, TrainingRoutine, Trainingsplan, ÜbungenKrafttraining, TrainingsplanÜbung, Trainingsplan_TrainingRoutine, KrafttrainingInstanz, TrainingsplanÜbungenKrafttraining, AusführungSatz, AusführungWid
from datetime import date
import json
import pprint
from .workout_konstrukt import generiere_trainingsplan_struktur
from datetime import datetime
import os
#import new_training_excice

from django.template import RequestContext
@login_required
def overview_view(request):
   # new_training_excice.big_data()
    print("\n"*5)
    print("over_view HALLLLLOOO")
    print("\n"*5)
    try:
         print(request.POST)
    except Exception as e:
        print("fail")
    if request.method == 'POST' and request.POST.get('aktivität'):
        #print("gefunden")
        write_aktivität_into_model(request)
    elif request.method == 'POST' and request.POST.get("addworktype") == 'addworktype': #request.POST.get('addworktype')
         #print(request.POST.get('addworktype'))
         write_workout_type_into_model(request)
    elif request.method == 'POST' and request.POST.get("editworktype") == 'editworktype':
         edit_workout_routine_in_model(request)
    elif request.method == 'POST' and request.POST.get("delete") == 'delete':
         delete_workout_type(request)
    elif request.method == 'POST' and request.POST.get("create Trainingplan ") == 'create Trainingplan':
        #print("halooooo create Trainingplan")
        id_TR = create_training_plan_into_model(request)
        TrainingplanÜbung = create_TrainingsplanÜbung_into_model(request, id_TR)
        create_Trainingsplan_TrainingRoutine(request, id_TR)
        #print(f"true or FALE: {TrainingplanÜbung}")
        if TrainingplanÜbung:
            print("IF ERFOLGT  sadsad a")
            #template_uebung_trainingplan_satz_wid(request, id_TR)
    elif request.method == 'POST' and request.POST.get("new trainingsplan") == 'new trainingsplan':
        edit_trainingsplan(request)
        edit_TrainingsplanÜbung(request)
    elif  request.method == 'POST' and request.POST.get("Create Instanz") == "Create Instanz":
        os.system('clear')
        try:
         print(request.POST)
        except Exception as e:
         print("fail")
        create_instaz_into_model(request)
    elif request.method == 'POST':
        return choice_workout_opinion(request)
    else:
        print("nicht gefunden")
    return render(request, 'workout/overview.html')



def create_instaz_into_model(request_):
    Object_trainingsplan = KrafttrainingInstanz.objects.create(
        trainingsplan =  Trainingsplan.objects.get(id=request_.POST.get("id_trainingsplan")),  # Aktuell eingeloggter Nutzer id_trainingsplan
        #datum = datetime.fromisoformat(date.today().isoformat)          
    )
    create_TrainingsplanÜbungenKrafttraining_into_model(request_, Object_trainingsplan)

def create_TrainingsplanÜbungenKrafttraining_into_model(request_, instanz_KrafttrainingInstanz):
    list_obj = []
    for ub in request_.POST.getlist("ÜbungenKrafttraining"):
        Object_trainingsplan = TrainingsplanÜbungenKrafttraining.objects.create(
            instanz = instanz_KrafttrainingInstanz,
          
            übung =  ÜbungenKrafttraining.objects.get(id=ub)  #ÜbungenKrafttraining         
        )
        print(f"create or mybe a TrainingsplanÜbungenKrafttraining : id: {Object_trainingsplan.id} | instanz: {instanz_KrafttrainingInstanz.id} | übung { ÜbungenKrafttraining.objects.get(id=ub)}")
        list_obj.append(Object_trainingsplan)
        create_AusführungSatz_into_model(request_, list_obj)

def create_AusführungSatz_into_model(request_, list_instanz_TrainingsplanÜbungenKrafttraining):
     #satz_list
    satz_list = request_.POST.getlist("satz_list")
    index = 0
    wied_ = 0
    for instanz_TrainingsplanÜbungenKrafttraining in list_instanz_TrainingsplanÜbungenKrafttraining:
        for satz_count in range(index, len(satz_list)-1):   
            Object_trainingsplan = AusführungSatz.objects.create(
                    training_übung = instanz_TrainingsplanÜbungenKrafttraining,
                    satz_nummer =  satz_list[satz_count]  #ÜbungenKrafttraining         
                )
            wied_ = create_AusführungWid_into_model(request_, satz_count, Object_trainingsplan, wied_)

            if satz_list[satz_count] > satz_list[satz_count + 1]:
                index = satz_count + 1
                continue
            
    Object_trainingsplan = AusführungSatz.objects.create(
                    training_übung = list_instanz_TrainingsplanÜbungenKrafttraining[-1],
                    satz_nummer =  satz_list[-1]  #ÜbungenKrafttraining         
                )
    create_AusführungWid_into_model(request_, index, Object_trainingsplan, wied_)

def create_AusführungWid_into_model(request_, index, instanz, index_wid=0):
    #print("hallo")
    wied_values = request_.POST.getlist("wid_value")
    for count in range(index_wid, len(wied_values)):
        #print(count)
        if wied_values[count] == "|":
            index_wid = count + 1
            continue
        else:
            value = wied_values[index_wid]
        #print(f"inhalt von wied_values {wied_values[count]} --- type: {type(wied_values[count])}")
        try: 
                wied_values[count] = int(wied_values[count])
        except ValueError as e:
               # print(f"EROR: {e}")
               pass
        if  isinstance(wied_values[count], (int, float)):
            print(f"instanz: {instanz} -- gewicht: {wied_values[count]}")
            Object_trainingsplan = AusführungWid.objects.create(
                            ausführung = instanz,
                            gewicht =  wied_values[count]     
                        )
    return index_wid + 1

# def overview(request):
#     if not request.user.is_pro:
#         return render(request, 'users/pro_required.html')
#     return render(request, "workout/overview.html")

def edit_TrainingsplanÜbung(request_):
    übung = request_.POST.getlist('übung')
    satz = request_.POST.getlist('satz')
    wiederholung = request_.POST.getlist('Wiederholung')
    exercise = request_.POST.getlist('übung')
    if exercise:
        create_TrainingsplanÜbung_into_model(request_, request_.POST.get('id_trainingsplan'))
        print("bin in exercice")
    if übung:
        if satz and wiederholung:
            for übung_, satz_, wiederholung_ in zip(request_.POST.getlist('übung'), request_.POST.getlist('satz'), request_.POST.getlist('Wiederholung')):
                TrainingsplanÜbung_obj = TrainingsplanÜbung.objects.get(id = übung_)
                TrainingsplanÜbung_obj.satz = satz_
                TrainingsplanÜbung_obj.wiederholung = wiederholung_
                TrainingsplanÜbung_obj.save()
                print(f"satz {satz_}, wied {wiederholung_}, übung {übung_}")
            print("war in satz / wied übung")
            
        elif satz:
            for übung, satz,  in zip( request_.POST.getlist('übung'), request_.POST.getlist('satz')):
                TrainingsplanÜbung_obj = TrainingsplanÜbung.objects.get(id = übung)
                TrainingsplanÜbung_obj.satz = satz
                TrainingsplanÜbung_obj.wiederholung = wiederholung
                TrainingsplanÜbung_obj.save()
        elif wiederholung:
            for übung, wiederholung in zip(request_.POST.getlist('übung'), request_.POST.getlist('Wiederholung')):
                TrainingsplanÜbung_obj = TrainingsplanÜbung.objects.get(id = übung)
                TrainingsplanÜbung_obj.satz = satz
                TrainingsplanÜbung_obj.wiederholung = wiederholung
                TrainingsplanÜbung_obj.save()


def edit_trainingsplan(request_):
    Trainingsplan_obj = Trainingsplan.objects.get(id = request_.POST.get('id_trainingsplan'))
    print("EDIT")
    if Trainingsplan_obj.user == request_.user :
        Trainingsplan_obj.name = request_.POST.get('name')
        Trainingsplan_obj.beschreibung = request_.POST.get('beschreibung')
        Trainingsplan_obj.save()

def create_training_plan_into_model(request_):
    if request_.method == 'POST':
        print("write_to  trainingsplan")
        name = request_.POST.get('name')
        beschreibung = request_.POST.get('beschreibung')
        print("schreibe WORKOUT TYPE ")
        # Neues TrainingRoutine-Objekt speichern
        Object_trainingsplan = Trainingsplan.objects.create(
            user = request_.user,  # Aktuell eingeloggter Nutzer
            name = name,
            beschreibung = beschreibung,
        )
        print("trainingsplan final")
        return Object_trainingsplan.id
        
def create_TrainingsplanÜbung_into_model(request_, id_TR):
    if request_.method == 'POST':
        if Trainingsplan.objects.filter(user=request_.user, id=id_TR).first(): # first könnte man streichen
            if request_.POST.get('exercise'):
                print("create_TrainingsplanÜbung_into_model")
                print(request_.POST.getlist('exercise'))                
                for Übung in request_.POST.getlist('exercise'):
                    try:
                            Übung = int(Übung)
                            print(f"Übung: {Übung}")
                    except ValueError as e:
                        continue
                    übung_instance = ÜbungenKrafttraining.objects.get(id=Übung)
                    trainingsplan_instance = Trainingsplan.objects.get(id=id_TR)
                    print(f"name: {übung_instance.name}")
                    TrainingsplanÜbung.objects.create(
                        übung=übung_instance,  
                        trainingsplan=trainingsplan_instance,
                    )
                    #print("FINAL B")
                return True
        else:
             print("FAIL B")
             return False
    else:
        #print("mega falsch POST")
        return False

def create_Trainingsplan_TrainingRoutine(request_, id_TR):
     if request_.method == 'POST':
            if Trainingsplan.objects.filter(user=request_.user, id=id_TR).first():
                if request_.POST.get('workoutroutine'):
                    #print("create_Trainingsplan_TrainingRoutine")               
                    for routine in request_.POST.get('workoutroutine'):
                        try:
                             routine = int(routine)
                        except ValueError as e:
                            continue
                        if TrainingRoutine.objects.filter(user=request_.user, id=routine).first():
                            trainingsplan_instance = Trainingsplan.objects.get(id=id_TR)
                            training_routine_instance = TrainingRoutine.objects.get(id=routine)

                            Trainingsplan_TrainingRoutine.objects.create(
                                trainingsplan=trainingsplan_instance,
                                training_routine=training_routine_instance,
)
                            #print("FINAL C")
                        else:
                             #print("wrong routine")
                             pass
                else:
                     #print("wrong Trainingsplan")
                     pass

def delete_workout_type(request_):
    if request_.method == 'POST':
        #print(" bin im delete ")
        # Neues TrainingRoutine-Objekt speicher
        routine = TrainingRoutine.objects.get(id = request_.POST.get('id'))
        print("EDIT")
        if routine.user == request_.user :
            routine.delete()
            #print("ins delete")
        else:
             #print("kein delete weil falsche ID ")
             pass
@login_required
def add_activity(request):
    aktivitäten = Aktivitäten.objects.all()
    #print("hier add acitivity sdsadsadsadsadsadasdsadasd")
    if request.method == 'POST':
        aktivität_id = request.POST.get('aktivität')
        selected_activity = Aktivitäten.objects.get(id=aktivität_id)
        # Hier kannst du mit der ausgewählten Aktivität weiterarbeiten
        # Zum Beispiel speichern oder eine Nachricht anzeigen
        return render(request, 'workout/add_activity.html', {
            'aktivität': aktivitäten,
            'selected_activity': selected_activity
        })

    return render(request, 'workout/add_activity.html', {'aktivitäten': aktivitäten})

def edit_workout_routine_in_model(request_):
     if request_.method == 'POST':
        print(" bin im edit ")
        # Neues TrainingRoutine-Objekt speichern
        routine = TrainingRoutine.objects.get(id = request_.POST.get('id'))
        print("EDIT")
        if routine.user == request_.user :
            routine.name = request_.POST.get('name')
            routine.beschreibung = request_.POST.get('beschreibung')
            routine.save()
            #print("ins finale")
        else:
             #print("kein EDIT weil falsche ID ")
             pass

     

# zum erstellen einerr neuen TrainingsRoutine
def write_workout_type_into_model(request_):
     if request_.method == 'POST':
        #print("write_to database trainingtype")
        name = request_.POST.get('name')
        beschreibung = request_.POST.get('beschreibung')
        #print("schreibe WORKOUT TYPE ")
        # Neues TrainingRoutine-Objekt speichern
        TrainingRoutine.objects.create(
            user=request_.user,  # Aktuell eingeloggter Nutzer
            name=name,
            beschreibung=beschreibung
        )
    # zum hinzufügen von Aktivitäten die man gemacht haben  
def write_aktivität_into_model(request_):
    if request_.method == 'POST':
        #print("write_to database")
        aktivität_id = request_.POST.get('aktivität')
        #print(f" value = |{aktivität_id}|")
        aktivität_id = int(request_.POST.get('aktivität'))
        
        aktivität_instance = Aktivitäten.objects.get(id=aktivität_id)

        datum = request_.POST.get('datum')
        dauer = request_.POST.get('dauer')
        distanz = request_.POST.get('distanz')
        puls = request_.POST.get('puls')
        max_puls = request_.POST.get('max_puls')
        höhenmeter = request_.POST.get('höhenmeter')
        #print(datum)

        AktivitätenUser.objects.create(
            user=request_.user,
            aktivität=aktivität_instance,
            datum=datum,
            dauer=dauer or None,
            distanz=distanz or None,
            puls=puls or None,
            max_puls=max_puls or None,
            höhenmeter=höhenmeter or None,
        )

        # Weiterleitung zur Übersicht oder Erfolgsmeldung
        return redirect("workout:overview")

    # GET-Anfrage: Aktivitäten für das Dropdown-Menü abrufen
    aktivitäten = Aktivitäten.objects.all()
    
    return render(request_, 'workout/overview.html')

def choice_workout_opinion(request_):
   
    button_value = request_.POST.get('button')
    #print(f"Hallo {button_value}")
        # Überprüfen, welcher Button geklickt wurde
    if button_value == 'Activity':
            # Hier kannst du den Wert an dein Formular übergeben und entsprechende Logik ausführen
            context = {
                "heutiges_datum": date.today(),
                "aktivitäten": Aktivitäten.objects.all(),
            }
            html_content = render_to_string('workout/add_activity.html', context, request=request_)
            
            return render(request_, 'workout/overview.html', {'html_content': html_content})
        
    elif button_value == 'Training concept':
            context = {
                "routines": TrainingRoutine.objects.filter(user=request_.user)
            }
            html_content = render_to_string('workout/workout_type.html', context, request=request_)
            return render(request_, 'workout/overview.html', {'html_content': html_content})
    elif button_value == 'erstelle neue Trainings Routine':
        context = {
                "value" : "addworktype",
                "name" : "addworktype",
                "button" : "Create Routine",
            }
        #print(context)
        html_content = render_to_string('workout/add_workout_type.html', context, request=request_)
        return render(request_, 'workout/overview.html', {'html_content': html_content})
    elif  'selected_routine' in request_.POST:    
            context = {
                "name" : "editworktype",
                "value" : "editworktype",
                "TrainingRoutine": TrainingRoutine.objects.get(id=request_.POST.get("selected_routine")),
                "button" : "edit Trainingsplan",
            }
            html_content = render_to_string('workout/add_workout_type.html', context, request=request_)
            context = {
                "name" : "delete",
                "value" : "delete",
                "TrainingRoutine": TrainingRoutine.objects.get(id=request_.POST.get("selected_routine")),
                "button" : "delete workout type",
            }
            
            html_content = html_content + render_to_string('workout/edit_workout_type.html', context, request=request_)
            return render(request_, 'workout/overview.html', {'html_content': html_content})
    elif button_value == "erstelle Trainingsplan":
            context = {
                "ÜbungenKrafttraining": ÜbungenKrafttraining.objects.all(),
                "workoutroutine" : TrainingRoutine.objects.filter(user_id = request_.user),
                "traininsplans" : Trainingsplan.objects.filter(user_id = request_.user),
            }
            #print(context)
            html_content = render_to_string('workout/overview_trainingsplan.html', context, request=request_)
            html_content = html_content +  render_to_string('workout/create_training_plan.html', context, request=request_)
            return render(request_, 'workout/overview.html', {'html_content': html_content})
    elif button_value == "Training Plan":
        context = {
                "traininsplans" : Trainingsplan.objects.filter(user_id = request_.user),
            }
        html_content = render_to_string('workout/overview_trainingsplan.html', context, request=request_)
        return render(request_, 'workout/overview.html', {'html_content': html_content})
    elif 'selected_trainingsplan' in request_.POST:
        print("\n Hallo bin in selected trainingsplan \n")
        context = {
                "übung" : TrainingsplanÜbung.objects.filter(trainingsplan_id=request_.POST.get("selected_trainingsplan")),
                "ÜbungenKrafttraining": ÜbungenKrafttraining.objects.all(),
                "workoutroutine" : TrainingRoutine.objects.filter(user_id = request_.user),
                "traininsplans" : Trainingsplan.objects.filter(user_id = request_.user),
                "trainingsplan" : Trainingsplan.objects.get(id=request_.POST.get("selected_trainingsplan")),
            }
        obj = TrainingsplanÜbung.objects.filter(trainingsplan_id=request_.POST.get("selected_trainingsplan"))
        for übung in obj:
            print(übung.übung.name)
            print(übung.satz)
            print(übung.wiederholung)
            print(übung.id)
        html_content = render_to_string('workout/overview_trainingsplan.html', context, request=request_)    
        html_content = html_content + render_to_string('workout/uebung_trainingsplan_satz_wid.html', context, request=request_)
        
        #html_content = html_content + render_to_string('workout/edit_workout_type.html', context, request=request_)
        return render(request_, 'workout/overview.html', {'html_content': html_content})
    elif button_value == "Training Plan instanz":
         # workout_instanz.html
        context = {               
                "workoutroutine" : TrainingRoutine.objects.filter(user_id = request_.user),
                "traininsplans" : Trainingsplan.objects.filter(user_id = request_.user),
            }
        html_content = render_to_string('workout/overview_instanz.html', context, request=request_)
        return render(request_, 'workout/overview.html', {'html_content': html_content}) 
    elif 'selected_routine_instanz' in request_.POST and request_.POST.get("selected_routine_instanz"):
        
        context = {               
                "workoutroutine" : TrainingRoutine.objects.filter(user_id = request_.user),
                "traininsplans" : Trainingsplan.objects.filter(user_id = request_.user),
                "traininsplans_" : Trainingsplan_TrainingRoutine.objects.filter(training_routine_id = request_.POST.get("selected_routine_instanz"))

            }
        html_content = render_to_string('workout/overview_instanz.html', context, request=request_)
        html_content = html_content + render_to_string('workout/overview_instaz_routine.html', context, request=request_)
        print("html_content:")
        print(html_content)
        return render(request_, 'workout/overview.html', {'html_content': html_content})
    elif "selected_trainingsplan_instanz" in request_.POST and request_.POST.get("selected_trainingsplan_instanz"):
        print("kuckkuck")
        obj_übungen = TrainingsplanÜbung.objects.filter(trainingsplan_id=request_.POST.get("selected_trainingsplan_instanz"))
        #print(obj_übungen)
        
        trainingsplan_id = request_.POST.get("selected_trainingsplan_instanz")
        print(f"id vom Trainingsplan: {trainingsplan_id}")
        trainingsplan_struktur = generiere_trainingsplan_struktur(trainingsplan_id)
        context = {               
                "workoutroutine" : TrainingRoutine.objects.filter(user_id = request_.user),
                "traininsplans" : Trainingsplan.objects.filter(user_id = request_.user),
                "übung" : TrainingsplanÜbung.objects.filter(trainingsplan_id=request_.POST.get("selected_trainingsplan_instanz")),
                "choice_plan" : request_.POST.get("selected_routine_instanz"),
                "hauptebene": trainingsplan_struktur,
                "id_" : trainingsplan_id

            }
        # print(satz)
        # print(wied)
        html_content = render_to_string('workout/create_instanz.html', context, request=request_)
        html_content = html_content + render_to_string('workout/overview_instaz_routine.html', context, request=request_)
        return render(request_, 'workout/overview.html', {'html_content': html_content})
    return render(request_, 'workout/overview.html')



