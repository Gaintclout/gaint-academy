const API_URL=process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
export async function apiFetch(path:string,init:RequestInit={}){
  const response=await fetch(API_URL+path,{...init,credentials:"include",headers:{"Content-Type":"application/json",...(init.headers||{})}});
  if(!response.ok) throw new Error((await response.json().catch(()=>null))?.detail || "Request failed");
  return response.json();
}
