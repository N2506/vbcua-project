import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Establishes a connection to the local vbcua_db instance."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',         # Replace with your MySQL username if different
            password='password', # Replace with your exact MySQL Workbench password
            database='vbcua_db'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database Connection Error: {str(e)}")
        return None

def log_evaluation_session(topic, metrics, transcript, evaluation):
    """
    Inserts real-time speech analytics and semantic scores into the 
    AUDIO_FILE, TRANSCRIPT, and EVALUATION_RESULT tables sequentially.
    """
    conn = get_db_connection()
    if not conn:
        return False
        
    try:
        cursor = conn.cursor()
        
        # 1. Look up or Insert the Reference Concept ID mapping
        cursor.execute("SELECT ref_concept_id FROM REFERENCE_CONCEPT WHERE concept_title = %s", (topic,))
        ref_row = cursor.fetchone()
        if ref_row:
            ref_concept_id = ref_row[0]
        else:
            # Fallback insertion if placeholder concept text is missing
            cursor.execute(
                "INSERT INTO REFERENCE_CONCEPT (concept_title, concept_text) VALUES (%s, %s)",
                (topic, f"Predefined ground truth definition for {topic}")
            )
            ref_concept_id = cursor.lastrowid
            
        # 2. Log metadata entries to AUDIO_FILE (Assuming default User ID 1)
        cursor.execute(
            "INSERT INTO AUDIO_FILE (user_id, file_name, file_path, duration_sec, status) VALUES (%s, %s, %s, %s, %s)",
            (1, "live_user_upload.mp3", "uploads/1.mp3", metrics.get("duration_sec", 0.0), "Processed")
        )
        audio_id = cursor.lastrowid
        
        # 3. Log values to TRANSCRIPT table
        cursor.execute(
            "INSERT INTO TRANSCRIPT (audio_id, transcript_text) VALUES (%s, %s)",
            (audio_id, transcript)
        )
        
        # 4. Log outputs to EVALUATION_RESULT table
        cursor.execute(
            "INSERT INTO EVALUATION_RESULT (audio_id, ref_concept_id, overall_score, understanding_level, notes) VALUES (%s, %s, %s, %s, %s)",
            (audio_id, ref_concept_id, evaluation.get("score", 0.0), evaluation.get("level", "Moderate"), evaluation.get("feedback", ""))
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Data logging execution failed: {str(e)}")
        if conn.is_connected():
            conn.rollback()
        return False
