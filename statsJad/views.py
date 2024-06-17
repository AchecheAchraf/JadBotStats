from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta
from django.http import HttpResponse
import re


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

from datetime import datetime
from django.db import connection
from django.shortcuts import render



from django.shortcuts import render
from datetime import datetime
from django.db import connection

def protocol(request):
    # Get values from the form
    start_date_str = request.POST.get('date-start')
    end_date_str = request.POST.get('date-end')
    protocol_name = request.POST.get('protocol-select')

    # Convert form dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Format dates to 'dd/mm/yyyy'
    formatted_start_date = start_date.strftime('%d/%m/%Y')
    formatted_end_date = end_date.strftime('%d/%m/%Y')

    # Define the list of all protocol names
    all_protocols = [
        "Entretien courant",
        "Chambre à blanc",
        "Entretien courant Expert+",
        "Entretien courant Avancé"
    ]

    with connection.cursor() as cursor:
        if protocol_name == "Tous les protocols":
            # If "Tous les protocols" is selected, search for all protocols
            query = f"""
                SELECT 
                    EXTRACT(EPOCH FROM (pe."end" - pe.start)) / 60 AS duration_minutes
                FROM 
                    protocol_event pe
                INNER JOIN 
                    protocol p ON pe.protocol_id = p.protocol_id
                WHERE 
                    p.protocol_name IN %s
                    AND pe.start >= %s
                    AND pe."end" <= %s
                    AND EXTRACT(EPOCH FROM (pe."end" - pe.start)) > 0
            """
            cursor.execute(query, [tuple(all_protocols), start_date, end_date])
        else:
            # Otherwise, search for the specific protocol selected
            query = """
                SELECT 
                    EXTRACT(EPOCH FROM (pe."end" - pe.start)) / 60 AS duration_minutes
                FROM 
                    protocol_event pe
                INNER JOIN 
                    protocol p ON pe.protocol_id = p.protocol_id
                WHERE 
                    p.protocol_name = %s
                    AND pe.start >= %s
                    AND pe."end" <= %s
                    AND EXTRACT(EPOCH FROM (pe."end" - pe.start)) > 0
            """
            cursor.execute(query, [protocol_name, start_date, end_date])

        # Fetch all durations
        durations = cursor.fetchall()

    # Extract durations and filter out zero durations
    durations = [duration[0] for duration in durations if duration[0] > 0]
    
    # Calculate the average duration (excluding zero durations)
    avg_duration = round(sum(durations) / len(durations), 2) if durations else 0

    # Count the number of protocol events
    protocol_count = len(durations)

    # Count the number of durations with leading zeros
    leading_zero_count = sum(1 for duration in durations if re.match(r'^0+\.\d+', str(duration)))

    # Return the rounded average value along with the formatted dates, protocol, and leading zero count
    context = {
        'avg_duration': avg_duration,
        'start_date': formatted_start_date,
        'end_date': formatted_end_date,
        'protocol_name': protocol_name,
        'protocol_count': protocol_count,
        'leading_zero_count': leading_zero_count
    }
    return render(request, 'index.html', context)







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
    
    
    