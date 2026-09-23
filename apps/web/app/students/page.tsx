"use client";
import {FormEvent,useEffect,useState} from "react";
import {useRouter} from "next/navigation";
import {apiFetch,isAuthError} from "../../lib/api";
type Student={id:string;admission_no:string;name:string;email?:string;status:string};
type Me={permissions:string[]};
export default function StudentsPage(){
 const router=useRouter(); const [rows,setRows]=useState<Student[]>([]); const [me,setMe]=useState<Me|null>(null); const [form,setForm]=useState({admission_no:"",first_name:"",last_name:"",email:""}); const [error,setError]=useState("");
 async function load(){try{const [students,user]=await Promise.all([apiFetch("/students"),apiFetch("/auth/me")]);setRows(students.data);setMe(user.data)}catch(e){if(isAuthError(e))router.replace("/login");else setError(e instanceof Error?e.message:"Unable to load students")}}
 useEffect(()=>{load()},[]);
 async function submit(e:FormEvent){e.preventDefault();setError("");try{await apiFetch("/students",{method:"POST",body:JSON.stringify({...form,email:form.email||null})});setForm({admission_no:"",first_name:"",last_name:"",email:""});await load()}catch(e){setError(e instanceof Error?e.message:"Unable to create student")}}
 const canCreate=me?.permissions.includes("students.student.create")??false;
 return <main className="module-page"><header><div><p className="eyebrow">STUDENT MANAGEMENT</p><h1>Students</h1><p className="muted">{canCreate?"Tenant-scoped student registry.":"Linked students available to your account."}</p></div><button onClick={()=>router.push("/dashboard")} className="secondary">Dashboard</button></header>
 {error&&<p className="error">{error}</p>}
 <section className={canCreate?"two-column":"profile-grid"}>
 {canCreate&&<form className="panel" onSubmit={submit}><h2>Add student</h2><label>Admission No<input value={form.admission_no} onChange={e=>setForm({...form,admission_no:e.target.value})} required/></label><label>First name<input value={form.first_name} onChange={e=>setForm({...form,first_name:e.target.value})} required/></label><label>Last name<input value={form.last_name} onChange={e=>setForm({...form,last_name:e.target.value})}/></label><label>Email<input type="email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/></label><button>Add student</button></form>}
 <section className="panel"><h2>{canCreate?"Student registry":"Linked students"}</h2><div className="student-list">{rows.length?rows.map(s=><button className="student-row" key={s.id} onClick={()=>router.push("/students/"+s.id)}><span><strong>{s.name}</strong><small>{s.admission_no}</small></span><span className="status-pill">{s.status}</span></button>):<p className="muted">{canCreate?"No students yet.":"No linked students available."}</p>}</div></section></section></main>;
}
