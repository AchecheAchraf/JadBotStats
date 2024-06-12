from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta
from django.http import HttpResponse

def protocol_list_with_name(request):
    specific_protocol_name = "Entretien courant"
    
    with connection.cursor() as cursor:
        query = """
            SELECT 
                pe.id AS event_id, 
                pe.user_id, 
                pe.start, 
                pe."end", 
                p.protocol_name
            FROM 
                protocol_event pe
            INNER JOIN 
                protocol p ON pe.protocol_id = p.protocol_id
            WHERE 
                p.protocol_name = %s
        """
        cursor.execute(query, [specific_protocol_name])
        columns = [col[0] for col in cursor.description]
        protocol_events = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return render(request, 'protocol.html', {'protocol_events': protocol_events})

def protocol_list_with_name_last_month(request):
    today = datetime.today()
    first_day_of_this_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    specific_protocol_name = "Entretien courant"
    
    with connection.cursor() as cursor:
        query = """
            SELECT 
                pe.id AS event_id, 
                pe.user_id, 
                pe.start, 
                pe."end", 
                p.protocol_name,
                pe.ehpad_id
            FROM 
                protocol_event pe
            INNER JOIN 
                protocol p ON pe.protocol_id = p.protocol_id
            WHERE 
                p.protocol_name = %s
                AND pe.start >= %s
                AND pe."end" <= %s
        """
        cursor.execute(query, [specific_protocol_name, first_day_of_last_month, last_day_of_last_month])
        columns = [col[0] for col in cursor.description]
        protocol_events = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return render(request, 'protocol.html', {'protocol_events': protocol_events})

def protocol_list_last_month(request):
    today = datetime.today()
    first_day_of_this_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    protocol_names = [
        "Entretien courant",
        "Chambre à blanc",
        "Entretien courant Expert+",
        "Entretien courant Avancé"
    ]

    protocol_names_str = ', '.join(f"'{name}'" for name in protocol_names)
    
    with connection.cursor() as cursor:
        query = f"""
            SELECT 
                pe.id AS event_id, 
                pe.user_id, 
                pe.start, 
                pe."end", 
                p.protocol_name,
                pe.ehpad_id
            FROM 
                protocol_event pe
            INNER JOIN 
                protocol p ON pe.protocol_id = p.protocol_id
            WHERE 
                p.protocol_name IN ({protocol_names_str})
                AND pe.start >= %s
                AND pe."end" <= %s
        """
        cursor.execute(query, [first_day_of_last_month, last_day_of_last_month])
        columns = [col[0] for col in cursor.description]
        protocol_events = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return render(request, 'protocol.html', {'protocol_events': protocol_events})

def protocol_list(request):
    protocol_names = [
        "Entretien courant",
        "Chambre à blanc",
        "Entretien courant Expert+",
        "Entretien courant Avancé"
    ]
    
    protocol_names_str = ', '.join(f"'{name}'" for name in protocol_names)
    
    with connection.cursor() as cursor:
        query = f"""
            SELECT 
                pe.id AS event_id, 
                pe.user_id, 
                pe.start, 
                pe."end", 
                p.protocol_name,
                pe.ehpad_id
            FROM 
                protocol_event pe
            INNER JOIN 
                protocol p ON pe.protocol_id = p.protocol_id
            WHERE 
                p.protocol_name IN ({protocol_names_str})
        """
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        protocol_events = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return render(request, 'protocol.html', {'protocol_events': protocol_events})

def index(request):
    return render(request, 'index.html')


def form(request):
    if request.method == 'POST':
        start_date = request.POST.get('date-start')
        end_date = request.POST.get('date-end')
        protocol = request.POST.get('protocol-select')

        # Print the received data
        print("Start Date:", start_date)
        print("End Date:", end_date)
        print("Protocol:", protocol)

        return HttpResponse("Form submitted successfully!")
    else:
        return HttpResponse("Invalid request method.")