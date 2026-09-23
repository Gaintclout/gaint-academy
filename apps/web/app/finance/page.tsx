"use client";
import {FormEvent,useEffect,useState} from "react";
import {useRouter} from "next/navigation";
import {apiFetch,isAuthError} from "../../lib/api";

export default function Finance(){
 const router=useRouter();
 const [me,setMe]=useState<any>(null);
 const [plans,setPlans]=useState<any[]>([]);
 const [invoices,setInvoices]=useState<any[]>([]);
 const [students,setStudents]=useState<any[]>([]);
 const [plan,setPlan]=useState({name:"",amount:""});
 const [invoice,setInvoice]=useState({student_id:"",fee_plan_id:"",invoice_no:""});
 const [payment,setPayment]=useState({invoice_id:"",reference:"",amount:"",method:"CASH"});
 const [order,setOrder]=useState({invoice_id:"",provider:"UAT",provider_order_id:"",idempotency_key:""});
 const [error,setError]=useState("");const [message,setMessage]=useState("");

 async function load(){
  try{
   const user=await apiFetch("/auth/me");setMe(user.data);
   const p=user.data.permissions as string[];
   if(p.includes("finance.plan.view")){setPlans((await apiFetch("/finance/fee-plans")).data);setInvoices((await apiFetch("/finance/invoices")).data)}
   if(p.includes("finance.invoice.create"))setStudents((await apiFetch("/finance/billable-students")).data);
  }catch(e){if(isAuthError(e))router.replace("/login");else setError(e instanceof Error?e.message:"Unable to load finance workspace")}
 }
 useEffect(()=>{load()},[]);

 async function createPlan(e:FormEvent){e.preventDefault();setError("");try{await apiFetch("/finance/fee-plans",{method:"POST",body:JSON.stringify({name:plan.name,amount:plan.amount})});setPlan({name:"",amount:""});setMessage("Fee plan created.");await load()}catch(e){setError(e instanceof Error?e.message:"Unable to create fee plan")}}
 async function createInvoice(e:FormEvent){e.preventDefault();setError("");try{await apiFetch("/finance/invoices",{method:"POST",body:JSON.stringify(invoice)});setInvoice({student_id:"",fee_plan_id:"",invoice_no:""});setMessage("Invoice created.");await load()}catch(e){setError(e instanceof Error?e.message:"Unable to create invoice")}}
 async function recordPayment(e:FormEvent){e.preventDefault();setError("");try{await apiFetch("/finance/payments",{method:"POST",body:JSON.stringify({...payment,amount:payment.amount})});setPayment({invoice_id:"",reference:"",amount:"",method:"CASH"});setMessage("Payment recorded.");await load()}catch(e){setError(e instanceof Error?e.message:"Unable to record payment")}}
 async function initiatePayment(e:FormEvent){e.preventDefault();setError("");try{const body={...order,provider_order_id:order.provider_order_id||("uat-"+Date.now()),idempotency_key:order.idempotency_key||crypto.randomUUID()};const r=await apiFetch("/finance/payment-orders",{method:"POST",body:JSON.stringify(body)});setMessage("Payment order created: "+r.data.provider_order_id);setOrder({invoice_id:"",provider:"UAT",provider_order_id:"",idempotency_key:""})}catch(e){setError(e instanceof Error?e.message:"Unable to initiate payment")}}

 const p=me?.permissions||[];const canPlan=p.includes("finance.plan.manage"),canInvoice=p.includes("finance.invoice.create"),canRecord=p.includes("finance.payment.record"),canInitiate=p.includes("finance.payment.initiate");
 return <main className="module-page"><header><div><p className="eyebrow">FINANCE</p><h1>Fees & Billing</h1><p className="muted">Permission-scoped fee plans, invoices and payment workflows.</p></div><button className="secondary" onClick={()=>router.push("/dashboard")}>Dashboard</button></header>
 {message&&<p className="status">{message}</p>}{error&&<p className="error">{error}</p>}
 {(canPlan||canInvoice)&&<section className="two-column">{canPlan&&<form className="panel" onSubmit={createPlan}><h2>Create fee plan</h2><label>Plan name<input value={plan.name} onChange={e=>setPlan({...plan,name:e.target.value})} required/></label><label>Amount<input type="number" min="0.01" step="0.01" value={plan.amount} onChange={e=>setPlan({...plan,amount:e.target.value})} required/></label><button>Create plan</button></form>}
 {canInvoice&&<form className="panel" onSubmit={createInvoice}><h2>Create invoice</h2><label>Student<select value={invoice.student_id} onChange={e=>setInvoice({...invoice,student_id:e.target.value})} required><option value="">Select student</option>{students.map(x=><option key={x.id} value={x.id}>{x.name} · {x.admission_no}</option>)}</select></label><label>Fee plan<select value={invoice.fee_plan_id} onChange={e=>setInvoice({...invoice,fee_plan_id:e.target.value})} required><option value="">Select plan</option>{plans.map(x=><option key={x.id} value={x.id}>{x.name} · ₹ {x.amount}</option>)}</select></label><label>Invoice no<input value={invoice.invoice_no} onChange={e=>setInvoice({...invoice,invoice_no:e.target.value})} required/></label><button>Create invoice</button></form>}</section>}
 <section className="panel" style={{marginTop:18}}><h2>Invoices</h2>{invoices.length?invoices.map(x=><div className="simple-row" key={x.id}><span><strong>{x.invoice_no}</strong><small>₹ {x.amount} · Paid ₹ {x.paid_amount}</small></span><span className="status-pill">{x.status}</span></div>):<p className="muted">No invoices available.</p>}</section>
 {(canRecord||canInitiate)&&<section className="two-column" style={{marginTop:18}}>
 {canRecord&&<form className="panel" onSubmit={recordPayment}><h2>Record confirmed payment</h2><label>Invoice<select value={payment.invoice_id} onChange={e=>setPayment({...payment,invoice_id:e.target.value})} required><option value="">Select invoice</option>{invoices.filter(x=>x.status!=="PAID").map(x=><option key={x.id} value={x.id}>{x.invoice_no}</option>)}</select></label><label>Reference<input value={payment.reference} onChange={e=>setPayment({...payment,reference:e.target.value})} required/></label><label>Amount<input type="number" min="0.01" step="0.01" value={payment.amount} onChange={e=>setPayment({...payment,amount:e.target.value})} required/></label><label>Method<input value={payment.method} onChange={e=>setPayment({...payment,method:e.target.value})} required/></label><button>Record payment</button></form>}
 {canInitiate&&<form className="panel" onSubmit={initiatePayment}><h2>Initiate payment</h2><p className="muted">Creates a payment order only. It does not confirm money received.</p><label>Invoice<select value={order.invoice_id} onChange={e=>setOrder({...order,invoice_id:e.target.value})} required><option value="">Select invoice</option>{invoices.filter(x=>x.status!=="PAID").map(x=><option key={x.id} value={x.id}>{x.invoice_no}</option>)}</select></label><label>Provider<input value={order.provider} onChange={e=>setOrder({...order,provider:e.target.value})} required/></label><label>Provider order ID (optional for UAT)<input value={order.provider_order_id} onChange={e=>setOrder({...order,provider_order_id:e.target.value})}/></label><button>Initiate payment</button></form>}</section>}
 </main>
}