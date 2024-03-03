# Database Design

## Table 1: Department
<<<<<<< HEAD
=======

>>>>>>> master
- Fields:
  - ID
  - department_name
  - progress_percentage

## Table 2: Reports
<<<<<<< HEAD
=======

>>>>>>> master
- Fields:
  - ID
  - report_name
  - uploaded_by (relationship with users table)
  - actual_percentage
  - achieved_percentage
  - related_department (relationship with department table)
  - created_at
  - updated_at

## Table 3: Users
<<<<<<< HEAD
=======

>>>>>>> master
- Fields:
  - ID
  - name
  - department (relationship with department table)
  - uploaded_report_url (relationship with reports)

# APIs Design

## Admin APIs
<<<<<<< HEAD
=======

>>>>>>> master
- POST: /add_department
- POST: /create_report_type
- POST: /add_report_metrics/{report_id: int}
- POST: /create_user
- GET: /get_departments
- GET: /get_uploaded_reports
- GET: /get_uploaded_report_by_employee
- GET: /get_admin_info
- GET: /get_stats
- GET: /get_users
- GET: /get_user_byID

## Employee APIs
<<<<<<< HEAD
=======

>>>>>>> master
- POST: {multipart} /upload
- GET: /uploaded_reports
- GET: /employee_info

# Features Design

## Admin View
<<<<<<< HEAD
=======

>>>>>>> master
- Show all departments.
- Inside each department, display the uploaded reports.
- Each report will have an actual weight (percentage) and an achieved weight, depending on whether it is completed or not based on the defined metrics by the admin.
- The uploaded report will have a sign indicating whether it is completed or not.
- The uploaded report will show the employee name who uploaded it, the upload time, and modification time if applicable.
- Show the overall progress percentage for each department's report, calculated automatically by summing up the percentages of the uploaded reports (unuploaded reports will be considered as 0%).

## Employee View
<<<<<<< HEAD
=======

>>>>>>> master
- Employee info display.
- Option to upload documents (reports).
- Ability to re-upload modified documents, with modifications being recorded by time.
- Show progress percentage and a sign indicating whether it has reached the full percentage or still needs work.
