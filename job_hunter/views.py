from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

@login_required
def dashboard_view(request):
    user_id = request.user.id
    stats = {}

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                COUNT(o.id) AS total_offers,
                COUNT(CASE WHEN o.response = 1 THEN 1 END) AS responded_offers,
                COUNT(CASE WHEN o.status IS NOT NULL AND o.status != 0 THEN 1 END) AS total_applications,
                COUNT(CASE WHEN o.status = 1 THEN 1 END) AS open_applications,
                COUNT(CASE WHEN o.status = 2 THEN 1 END) AS applied_applications,
                COUNT(CASE WHEN o.status = 3 THEN 1 END) AS rejected_applications,
                COUNT(CASE WHEN o.status = 4 THEN 1 END) AS accepted_applications
            FROM users_customuser u
            LEFT JOIN job_hunter_offer o ON u.id = o.user_id
            WHERE u.id = %s
            GROUP BY u.id;
        """, [user_id])
        
        row = cursor.fetchone()
        if row:
            (stats["total_offers"], stats["responded_offers"], stats["total_applications"],
             stats["open_applications"], stats["applied_applications"],
             stats["rejected_applications"], stats["accepted_applications"]) = row

    return render(request, "job_hunter/dashboard.html", {"stats": stats})
