"use client";
import { useRouter } from "next/navigation";
import { apiFetch } from "../lib/api";
export default function LogoutButton(){
  const router=useRouter();
  async function logout(){try{await apiFetch("/auth/logout",{method:"POST"});}finally{router.replace("/login");}}
  return <button className="logout" onClick={logout}>Sign out</button>;
}
