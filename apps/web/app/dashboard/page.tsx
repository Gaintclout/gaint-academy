export default function Dashboard(){
  return <main className="dashboard-shell"><aside><div className="logo">GA</div><strong>GAINT Academy</strong><nav><a className="active">Dashboard</a><a>Students</a><a>Academics</a><a>Attendance</a><a>Reports</a><a>Settings</a></nav></aside>
  <section className="workspace"><header><div><p className="eyebrow">INSTITUTION ADMIN</p><h1>Dashboard</h1></div><span className="status-pill">Stage 0</span></header>
  <div className="welcome"><h2>Foundation workspace</h2><p>Tenant, identity, RBAC, audit and secure session foundations are being established before academic modules are enabled.</p></div>
  <div className="metric-grid"><article><span>Platform</span><strong>Online</strong></article><article><span>Tenant isolation</span><strong>Enabled</strong></article><article><span>RBAC</span><strong>Foundation</strong></article><article><span>Audit</span><strong>Enabled</strong></article></div>
  </section></main>;
}
