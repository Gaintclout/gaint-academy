"use client";
import { useEffect,useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "../../lib/api";
import LogoutButton from "../../components/LogoutButton";
type Me={email:string;permissions:string[]};
type Summary={platform:string;tenant_isolation:string;rbac:string;audit:string};
export default function DashboardClient(){
 const router=useRouter(); const [me,setMe]=useState<Me|null>(null); const [s,setS]=useState<Summary|null>(null);
 useEffect(()=>{Promise.all([apiFetch("/auth/me"),apiFetch("/dashboard/summary")]).then(([m,d])=>{setMe(m.data);setS(d.data)}).catch(()=>router.replace("/login"));},[router]);
 if(!me||!s) return <main className="loading">Loading secure workspace…</main>;
 return <main className="dashboard-shell"><aside><div className="logo">GA</div><strong>GAINT Academy</strong><nav><a className="active">Dashboard</a><a href="/students">Students</a><a href="/academics">Academics</a><a href="/staff">Staff</a><a>Attendance</a><a>Reports</a><a>Settings</a></nav></aside>
 <section className="workspace"><header><div><p className="eyebrow">INSTITUTION ADMIN</p><h1>Dashboard</h1><p className="muted">{me.email}</p></div><div className="header-actions"><span className="status-pill">Stage 0</span><LogoutButton/></div></header>
 <div className="welcome"><h2>Foundation workspace</h2><p>Authenticated tenant context, permissions, audit and secure sessions are active.</p></div>
 <div className="metric-grid"><article><span>Platform</span><strong>{s.platform}</strong></article><article><span>Tenant isolation</span><strong>{s.tenant_isolation}</strong></article><article><span>RBAC</span><strong>{s.rbac}</strong></article><article><span>Audit</span><strong>{s.audit}</strong></article></div>
 </section></main>;
}
