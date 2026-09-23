from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read_web(p):return (ROOT.parent/"web"/p).read_text(encoding="utf-8")

def test_students_page_hides_create_form_without_permission():
 s=read_web("app/students/page.tsx")
 assert 'students.student.create' in s
 assert 'const canCreate=' in s
 assert '{canCreate&&<form' in s
 assert 'Linked students available to your account.' in s
