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



def protocolrooms(request):
    # Get values from the form
    start_date_str = request.POST.get('date-start')
    end_date_str = request.POST.get('date-end')
    protocol_name = request.POST.get('protocol-select')

    # Convert form dates to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    query = """
        SELECT 
            r.room_number,
            COUNT(pp.room_id) AS protocol_event_count
        FROM 
            protocol_event pe
        LEFT JOIN 
            protocol p ON pe.protocol_id = p.protocol_id
        LEFT JOIN 
            room r ON pe.ehpad_id = r.ehpad_id
        WHERE 
            pe.start >= %s
            AND pe."end" <= %s
            AND p.protocol_name = %s
        GROUP BY 
            r.room_number
        ORDER BY 
            r.room_number
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date, protocol_name])
        results = cursor.fetchall()

    # Print the results in the terminal
    print(f"Protocols from {start_date_str} to {end_date_str} for protocol: {protocol_name}")
    print(results)
    for row in results:
        room_number = row[0]
        protocol_event_count = row[1]
        print(f"Room Number: {room_number}, Protocol Event Count: {protocol_event_count}")
    
    return HttpResponse("The results have been printed in the terminal.")

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
    
    
    
    
    
    
from io import BytesIO
import base64
from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
# Import facultatif pour afficher joliment les résultats dans un tableau
from tabulate import tabulate
from django.db import connection


from django.shortcuts import render
from django.db import connection
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def graph_protocol_task_counts(request):
    # Exécution de la requête SQL pour récupérer les données
    with connection.cursor() as cursor:
        query = """
            SELECT p.protocol_id, p.protocol_name, COUNT(pt.id) AS task_count
            FROM protocol p
            LEFT JOIN protocol_task pt ON p.protocol_id = pt.protocol_id
            GROUP BY p.protocol_id, p.protocol_name
            ORDER BY p.protocol_name;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

    # Afficher les résultats dans le terminal
    headers = ["Protocol ID", "Protocol Name", "Task Count"]
    print("\nRésultats dans le terminal:")
    for row in rows:
        print(row)

    # Extraction des données pour le graphique
    protocol_names = [row[1] for row in rows]  # Noms des protocoles
    task_counts = [row[2] for row in rows]     # Nombre de tâches

    # Création du graphique à barres avec Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(protocol_names, task_counts, color='blue')
    plt.xlabel('Protocole')
    plt.ylabel('Nombre de Tâches')
    plt.title('Nombre de Tâches par Protocole')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Conversion du graphique en image pour l'intégrer dans le template
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Renvoyer le résultat dans le template
    context = {'image_base64': image_base64}
    return render(request, 'index.html', context)
