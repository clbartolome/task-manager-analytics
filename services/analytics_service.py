import pandas as pd
from sqlalchemy import text

def get_task_statistics(db):

    with db.engine.connect() as conn:
        query = "SELECT completed, completion_date, due_date, COUNT(*) as count FROM task GROUP BY completed,completion_date, due_date;"
        result = conn.execute(text(query))

    df = pd.DataFrame(result.fetchall(), columns=result.keys())

    total_tasks = df['count'].sum()
    completed_tasks = df[df['completed'] == 1]['count'].sum() if 'completed' in df['completed'] else 0
    incomplete_tasks = df[df['completed'] == 0]['count'].sum() if 'completed' in df['completed'] else 0

   # Convert completion_date to string to use as dictionary keys
    df['completion_date_str'] = df['completion_date'].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    completed_by_date = df[df['completed'] == 1].groupby('completion_date_str')['count'].sum().to_dict()
        
    df['completion_time'] = (pd.to_datetime(df['completion_date']) - pd.to_datetime(df['due_date'])).dt.days
    avg_completion_time = df[df['completed'] == 1]['completion_time'].mean()

    stats = {
        'total_tasks': int(total_tasks),
        'completed_tasks': int(completed_tasks),
        'incomplete_tasks': int(incomplete_tasks),
        'completed_by_date': completed_by_date,
        'avg_completion_time': avg_completion_time
    }
    return stats
