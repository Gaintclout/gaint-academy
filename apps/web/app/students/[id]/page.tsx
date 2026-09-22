"use client";
import {useEffect,useState} from "react";
import {useParams,useRouter} from "next/navigation";
import {apiFetch} from "../../../lib/api";
export default function Student360(){
 const {id}=useParams<{id:string}>(); const router=useRouter(); const [s,setS]=useState<any>(null);
 useEffect(()=>{apiFetch("/students/"+id).then(x=>setS(x.data)).catch(()=>router.replace("/students"))},[id,router]);
 if(!s)return <main className="loading">Loading Student 360…</main>;
 return <main className="module-page"><header><div><p className="eyebrow">STUDENT 360</p><h1>{s.first_name} {s.last_name||""}</h1><p className="muted">{s.admission_no}</p></div><button className="secondary" onClick={()=>router.push("/students")}>Back</button></header>
 <section className="profile-grid"><article className="panel"><h2>Profile</h2><dl><dt>Email</dt><dd>{s.email||"—"}</dd><dt>Status</dt><dd>{s.status}</dd></dl></article><article className="panel"><h2>Current enrollment</h2>{s.enrollment?<dl><dt>Academic Year</dt><dd>{s.enrollment.academic_year_id}</dd><dt>Class</dt><dd>{s.enrollment.class_id}</dd><dt>Section</dt><dd>{s.enrollment.section_id}</dd></dl>:<p className="muted">Not enrolled yet.</p>}</article></section></main>;
}
