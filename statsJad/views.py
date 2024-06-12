from django.shortcuts import render
from django.db import connection

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
                pe.id, pe.user_id, pe.start, pe."end", p.protocol_name
            FROM 
                protocol_event pe
            INNER JOIN 
                protocol p ON pe.protocol_id = p.protocol_id
            WHERE 
                p.protocol_name IN ({protocol_names_str})
        """
        cursor.execute(query)
        protocol_events = cursor.fetchall()

    return render(request, 'protocol.html', {'protocol_events': protocol_events})
