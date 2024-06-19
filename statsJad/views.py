from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta
from django.http import HttpResponse
import plotly.graph_objs as go
from collections import defaultdict
import re
from plotly.subplots import make_subplots


def generate_protocols_per_day_graph(start_date, end_date, protocol_name):
    # Query to get the number of protocols done per day
    with connection.cursor() as cursor:
        if protocol_name == "Tous les protocols":
            query = """
                SELECT DATE(start) as day, COUNT(*) as protocol_count
                FROM protocol_event
                WHERE start >= %s AND start <= %s
                GROUP BY DATE(start)
                ORDER BY day
            """
            cursor.execute(query, [start_date, end_date])
        else:
            query = """
                SELECT DATE(pe.start) as day, COUNT(*) as protocol_count
                FROM protocol_event pe
                JOIN protocol p ON pe.protocol_id = p.protocol_id
                WHERE pe.start >= %s AND pe.start <= %s AND p.protocol_name = %s
                GROUP BY DATE(pe.start)
                ORDER BY day
            """
            cursor.execute(query, [start_date, end_date, protocol_name])

        results = cursor.fetchall()

    # Prepare data for the graph
    dates = [result[0] for result in results]
    protocol_counts = [result[1] for result in results]

    # Create the bar plot
    trace_jour = go.Bar(
        x=dates,
        y=protocol_counts,
        name='Nombre de protocols par jour'
    )

    layout = go.Layout(
        title='Nombre de protocols par jour',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Nombre de Protocols'),
    )

    fig = go.Figure(data=[trace_jour], layout=layout)

    # Update layout for legend and graph title
    fig.update_layout(
        legend=dict(orientation='v', yanchor='bottom', y=0.3, xanchor='center', x=1.2),
        title_font=dict(size=20, family='Arial')
    )

    # Convert the figure to an HTML string
    graph_html = fig.to_html(full_html=False)

    return graph_html


def index(request):
    return render(request, 'index.html')



import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime

import re
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from io import BytesIO
import base64
from django.db import connection
from datetime import datetime


def generate_avg_duration_per_day_graph(start_date, end_date, protocol_name):
    all_protocols = [
        "Entretien courant",
        "Chambre à blanc",
        "Entretien courant Expert+",
        "Entretien courant Avancé"
    ]
    with connection.cursor() as cursor:
        if protocol_name == "Tous les protocols":
            query = """
                SELECT 
                    DATE(pe.start) as day, 
                    AVG(EXTRACT(EPOCH FROM (pe."end" - pe.start)) / 60) as avg_duration_minutes
                FROM 
                    protocol_event pe
                JOIN 
                    protocol p ON pe.protocol_id = p.protocol_id
                WHERE 
                    pe.start >= %s AND pe.start <= %s AND p.protocol_name IN %s
                GROUP BY 
                    DATE(pe.start)
                ORDER BY 
                    day
            """
            cursor.execute(query, [start_date, end_date, tuple(all_protocols)])
        else:
            query = """
                SELECT 
                    DATE(pe.start) as day, 
                    AVG(EXTRACT(EPOCH FROM (pe."end" - pe.start)) / 60) as avg_duration_minutes
                FROM 
                    protocol_event pe
                JOIN 
                    protocol p ON pe.protocol_id = p.protocol_id
                WHERE 
                    pe.start >= %s AND pe.start <= %s AND p.protocol_name = %s
                GROUP BY 
                    DATE(pe.start)
                ORDER BY 
                    day
            """
            cursor.execute(query, [start_date, end_date, protocol_name])

        results = cursor.fetchall()

    days = [result[0] for result in results]
    avg_durations = [result[1] for result in results]

    fig = make_subplots()
    trace = go.Scatter(
        x=days,
        y=avg_durations,
        mode='lines+markers+text',
        text=[f'{avg:.2f}' for avg in avg_durations],
        textposition='top center',
        marker=dict(size=10),
        line=dict(width=2, color='blue')
    )

    fig.add_trace(trace)
    fig.update_layout(
        title=f'Durée moyenne pour\n{protocol_name}',
        xaxis_title='Date',
        yaxis_title='Durée moyenne minutes',
        xaxis=dict(tickformat='%Y-%m-%d'),
        autosize=True,
        height=450,
    )

    graph_html = fig.to_html(full_html=False)
    return graph_html

def generate_tasks_count_graph(start_date, end_date):
    all_protocols = [
        "Entretien courant",
        "Chambre à blanc",
        "Entretien courant Expert+",
        "Entretien courant Avancé"
    ]

    with connection.cursor() as cursor:
        # Query to get the count of tasks for each protocol
        query = """
            SELECT p.protocol_name, COUNT(te.id) as task_count
            FROM task_event te
            JOIN protocol_task pt ON te.protocol_task_id = pt.id
            JOIN protocol p ON pt.protocol_id = p.protocol_id
            WHERE p.protocol_name IN %s AND te.start >= %s AND te.end <= %s
            GROUP BY p.protocol_name
        """
        cursor.execute(query, [tuple(all_protocols), start_date, end_date])
        results = cursor.fetchall()

    # Prepare data for the graph
    protocol_names = [result[0] for result in results]
    task_counts = [result[1] for result in results]

    # Create the bar plot
    trace = go.Bar(
        x=protocol_names,
        y=task_counts,
        name='Number of Tasks'
    )

    layout = go.Layout(
        title='Nombre de tâchse par protocol',
        xaxis=dict(title='Protocol'),
        yaxis=dict(title='Nombre de tâches'),
    )

    fig = go.Figure(data=[trace], layout=layout)

    # Convert the figure to an HTML string
    graph_html = fig.to_html(full_html=False)
    
    return graph_html

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

    graph_html = generate_protocols_per_day_graph(start_date, end_date, protocol_name)

    avg_duration_graph_html = generate_avg_duration_per_day_graph(start_date, end_date, protocol_name)
    pie_graph_html = plot_is_valid_pie()
    


    graph_html_tasks_count = generate_tasks_count_graph(start_date, end_date)


    # Return the rounded average value along with the formatted dates, protocol, and leading zero count
    context = {
        'avg_duration': avg_duration,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'protocol_name': protocol_name,
        'protocol_count': protocol_count,
        'leading_zero_count': leading_zero_count,
        'graph_html': graph_html,
        'avg_duration_graph_html': avg_duration_graph_html,
        'graph_html_tasks_count': graph_html_tasks_count ,
        'pie_graph_html':pie_graph_html,
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


import io
import base64
from datetime import datetime
from django.shortcuts import render
from django.db import connection
import matplotlib.pyplot as plt

def plot_is_valid_pie():
    # Perform raw SQL query to get counts of is_valid values
    query = """
        SELECT COUNT(id) AS total_events, SUM(CASE WHEN is_valid THEN 1 ELSE 0 END) AS valid_count
        FROM audit_element_event
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        total_events = row[0]
        valid_count = row[1]
        invalid_count = total_events - valid_count  # Calculate invalid count

    # Create data for Plotly pie chart
    labels = ['Valid', 'Invalid']
    values = [valid_count, invalid_count]
    colors = ['#1f77b4', '#ff7f0e']  # Blue for Valid, Orange for Invalid

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='percent',
                                 marker_colors=colors, hole=0.7)])

    fig.update_layout(
        title='Valid vs Invalid Audit Element Events',
        height=500,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # Convert plot to HTML
    graph_html = fig.to_html(full_html=False)

    return graph_html

def generate_avg_duration_per_day_graph(start_date, end_date, protocol_name):
    with connection.cursor() as cursor:
        if protocol_name == "Tous les protocols":
            query = """
                SELECT 
                    DATE(pe.start) as day, 
                    AVG(EXTRACT(EPOCH FROM (pe."end" - pe.start)) / 60) as avg_duration_minutes
                FROM 
                    protocol_event pe
                JOIN 
                    protocol p ON pe.protocol_id = p.protocol_id
                WHERE 
                    pe.start >= %s AND pe.start <= %s
                GROUP BY 
                    DATE(pe.start)
                ORDER BY 
                    day
            """
            cursor.execute(query, [start_date, end_date])
        else:
            query = """
                SELECT 
                    DATE(pe.start) as day, 
                    AVG(EXTRACT(EPOCH FROM (pe."end" - pe.start)) / 60) as avg_duration_minutes
                FROM 
                    protocol_event pe
                JOIN 
                    protocol p ON pe.protocol_id = p.protocol_id
                WHERE 
                    pe.start >= %s AND pe.start <= %s AND p.protocol_name = %s
                GROUP BY 
                    DATE(pe.start)
                ORDER BY 
                    day
            """
            cursor.execute(query, [start_date, end_date, protocol_name])

        results = cursor.fetchall()

    days = [result[0] for result in results]
    avg_durations = [result[1] for result in results]

    fig = make_subplots()
    trace = go.Scatter(
        x=days,
        y=avg_durations,
        mode='lines+markers+text',
        text=[f'{avg:.2f}' for avg in avg_durations],
        textposition='top center',
        marker=dict(size=10),
        line=dict(width=2, color='blue')
    )

    fig.add_trace(trace)
    fig.update_layout(
        title=f'Durée moyenne pour\n{protocol_name}',
        xaxis_title='Date',
        yaxis_title='Durée moyenne minutes',
        xaxis=dict(tickformat='%Y-%m-%d'),
        autosize=True,
        height=450,
    )

    graph_html = fig.to_html(full_html=False)
    return graph_html
