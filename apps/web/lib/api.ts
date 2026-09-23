const API_URL=process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const SAFE_METHODS=new Set(["GET","HEAD","OPTIONS"]);
const PUBLIC_MUTATIONS=new Set(["/auth/login","/auth/forgot-password","/auth/reset-password"]);
let csrfToken:string|null=null;

async function ensureCsrf(){
  if(csrfToken)return csrfToken;
  const response=await fetch(API_URL+"/auth/csrf",{credentials:"include"});
  if(!response.ok)throw new Error((await response.json().catch(()=>null))?.detail || "Unable to initialize secure session");
  const body=await response.json();
  csrfToken=body.data?.csrf_token || null;
  if(!csrfToken)throw new Error("Unable to initialize secure session");
  return csrfToken;
}

export async function apiFetch(path:string,init:RequestInit={}){
  const method=(init.method||"GET").toUpperCase();
  const headers:Record<string,string>={"Content-Type":"application/json",...((init.headers||{}) as Record<string,string>)};
  if(!SAFE_METHODS.has(method)&&!PUBLIC_MUTATIONS.has(path)){
    headers["X-CSRF-Token"]=await ensureCsrf();
  }
  const response=await fetch(API_URL+path,{...init,credentials:"include",headers});
  if(response.status===403&&!SAFE_METHODS.has(method)&&!PUBLIC_MUTATIONS.has(path)){
    csrfToken=null;
  }
  if(!response.ok) throw new Error((await response.json().catch(()=>null))?.detail || "Request failed");
  return response.json();
}
