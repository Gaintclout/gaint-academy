"use client";
import {FormEvent,useEffect,useState} from "react";
import {useRouter} from "next/navigation";
import {apiFetch,isAuthError} from "../../lib/api";

type SectionOption={id:string;label:string};
type RosterRow={student_id:string;admission_no:string;name:string;status:string;remark:string};

export default function Attendance(){
 const router=useRouter();
 const [sections,setSections]=useState<SectionOption[]>([]);
 const [section,setSection]=useState("");
 const [date,setDate]=useState("");
 const [session,setSession]=useState<any>(null);
 const [roster,setRoster]=useState<RosterRow[]>([]);
 const [records,setRecords]=useState<any[]>([]);
 const [me,setMe]=useState<any>(null);
 const [error,setError]=useState("");
 const [message,setMessage]=useState("");

 async function load(){
  try{
   const user=await apiFetch("/auth/me");setMe(user.data);
   if(user.data.permissions.includes("attendance.session.create"))setSections((await apiFetch("/attendance/sections")).data);
   if(user.data.permissions.includes("attendance.session.view"))setRecords((await apiFetch("/attendance/records")).data);
  }catch(e){if(isAuthError(e))router.replace("/login");else setError(e instanceof Error?e.message:"Unable to load attendance")}
 }
 useEffect(()=>{load()},[]);

 async function loadRoster(sectionId:string){
  setSection(sectionId);setRoster([]);setSession(null);setMessage("");setError("");
  if(!sectionId)return;
  try{
   const rows=(await apiFetch("/attendance/roster?section_id="+sectionId)).data;
   setRoster(rows.map((x:any)=>({...x,status:"PRESENT",remark:""})));
  }catch(e){setError(e instanceof Error?e.message:"Unable to load roster")}
 }

 async function create(e:FormEvent){
  e.preventDefault();setError("");setMessage("");
  try{
   const created=(await apiFetch("/attendance/sessions",{method:"POST",body:JSON.stringify({section_id:section,attendance_date:date})})).data;
   setSession(created);setMessage("Attendance session created. Mark the complete roster before submitting.");
  }catch(e){setError(e instanceof Error?e.message:"Unable to create session")}
 }

 function updateRoster(studentId:string,key:"status"|"remark",value:string){
  setRoster(rows=>rows.map(x=>x.student_id===studentId?{...x,[key]:value}:x));
 }

 async function saveRecords(){
  if(!session)return;
  setError("");setMessage("");
  try{
   const payload=roster.map(({student_id,status,remark})=>({student_id,status,remark:remark||null}));
   await apiFetch("/attendance/sessions/"+session.id+"/records",{method:"PUT",body:JSON.stringify(payload)});
   setMessage("Attendance roster saved.");
  }catch(e){setError(e instanceof Error?e.message:"Unable to save attendance roster")}
 }

 async function submit(){
  if(!session)return;
  setError("");setMessage("");
  try{
   await saveRecords();
   const submitted=(await apiFetch("/attendance/sessions/"+session.id+"/submit",{method:"POST"})).data;
   setSession(submitted);setMessage("Attendance submitted successfully.");await load();
  }catch(e){setError(e instanceof Error?e.message:"Unable to submit")}
 }

 const canCreate=me?.permissions?.includes("attendance.session.create");
 return <main className="module-page">
  <header><div><p className="eyebrow">DAILY OPERATIONS</p><h1>Attendance</h1><p className="muted">{canCreate?"Create, mark and submit section attendance.":"Submitted attendance available to your account."}</p></div><button className="secondary" onClick={()=>router.push("/dashboard")}>Dashboard</button></header>
  {message&&<p className="status">{message}</p>}{error&&<p className="error">{error}</p>}
  <section className={canCreate?"two-column":"profile-grid"}>
   {canCreate&&<form className="panel" onSubmit={create}><h2>New attendance session</h2><label>Section<select value={section} onChange={e=>loadRoster(e.target.value)} required><option value="">Select assigned section</option>{sections.map(x=><option key={x.id} value={x.id}>{x.label}</option>)}</select></label><label>Date<input type="date" value={date} onChange={e=>setDate(e.target.value)} required/></label><button disabled={!section||!date}>Create session</button></form>}
   <section className="panel"><h2>{canCreate?"Current session":"Attendance history"}</h2>{canCreate?(session?<><div className="simple-row"><strong>{session.id}</strong><span className="status-pill">{session.status}</span></div><p className="muted">{roster.length} active student(s) in the selected section.</p></>:<p className="muted">Select a section and create a session to begin.</p>):(records.length?records.map((x,i)=><div className="simple-row" key={x.student_id+"-"+x.attendance_date+"-"+i}><span><strong>{x.attendance_date}</strong><small>{x.remark||"No remark"}</small></span><span className="status-pill">{x.status}</span></div>):<p className="muted">No submitted attendance records available.</p>)}</section>
  </section>
  {canCreate&&session?.status==="DRAFT"&&<section className="panel" style={{marginTop:18}}><h2>Mark roster</h2>{roster.length?roster.map(x=><div className="simple-row" key={x.student_id}><span><strong>{x.name}</strong><small>{x.admission_no}</small></span><span style={{display:"flex",gap:8,alignItems:"center",flexWrap:"wrap"}}><select value={x.status} onChange={e=>updateRoster(x.student_id,"status",e.target.value)}><option value="PRESENT">Present</option><option value="ABSENT">Absent</option><option value="LATE">Late</option><option value="EXCUSED">Excused</option></select><input placeholder="Remark" value={x.remark} onChange={e=>updateRoster(x.student_id,"remark",e.target.value)}/></span></div>):<p className="muted">No active students are enrolled in this section.</p>}<div className="state-actions"><button type="button" onClick={saveRecords} disabled={!roster.length}>Save roster</button><button type="button" onClick={submit} disabled={!roster.length}>Submit attendance</button></div></section>}
 </main>
}