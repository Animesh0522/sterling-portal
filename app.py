import React, { useState, useEffect, useRef } from 'react';
import { 
  Shield, 
  FileText, 
  Upload, 
  Download, 
  Lock, 
  Menu, 
  X, 
  Phone, 
  MapPin, 
  Mail, 
  CheckCircle, 
  User, 
  LogOut, 
  Briefcase, 
  Globe, 
  TrendingUp,
  FileCheck,
  Cloud,
  Users,
  Key,
  AlertCircle,
  Settings,
  Save,
  Plus,
  Trash2,
  Activity,
  Smartphone,
  Server,
  HardDrive,
  RefreshCw,
  Sparkles,
  MessageSquare,
  Send,
  Bot,
  Copy,
  Info,
  Database
} from 'lucide-react';
import { initializeApp } from 'firebase/app';
import { 
  getAuth, 
  onAuthStateChanged, 
  signInWithCustomToken, 
  signInAnonymously, 
  signOut, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  updateProfile
} from 'firebase/auth';
import { 
  getFirestore, 
  collection, 
  addDoc, 
  onSnapshot, 
  query, 
  orderBy, 
  serverTimestamp,
  doc,
  setDoc,
  getDoc
} from 'firebase/firestore';

/**
 * ============================================================================
 * 🔧 FIRM CONFIGURATION
 * ============================================================================
 */
const MASTER_ADMIN_EMAIL = "private.client@sterlingstone.cpa"; 

const DEFAULT_CONFIG = {
  name: "Sterling & Stone CPA",
  tagline: "Global Wealth Preservation & Strategic Tax Compliance",
  principal: "Alexander Sterling, CPA, MST",
  address: "100 Financial District Blvd, Suite 4500, New York, NY 10005",
  phone: "+1 (212) 555-0199",
  email: "private.client@sterlingstone.cpa",
  license: "NY License #045-9921",
  security: { mfaEnabled: false, ipRestriction: true, lastAudit: "2025-10-15" },
  cloudStorage: { provider: "OneDrive", isConnected: false, rootFolder: "/SterlingStone_Secure_Vault", adminEmail: "admin@sterlingstone.cpa" }
};

const DEFAULT_ALLOWED_CLIENTS = ["client@example.com", "vip.family@wealth.com"];

// --- Firebase Setup ---
const firebaseConfig = JSON.parse(__firebase_config);
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';

// --- Types ---
type ViewState = 'home' | 'services' | 'portal' | 'contact' | 'about' | 'admin';
type AuthMode = 'login' | 'register' | 'mfa_verify';

interface Document {
  id: string; name: string; size: string; type: string;
  status: 'Pending Review' | 'Processed' | 'Action Required' | 'Synced to OneDrive';
  oneDrivePath: string; uploadDate: any;
}

interface FirmConfig {
  name: string; tagline: string; principal: string; address: string; phone: string; email: string; license: string;
  security: { mfaEnabled: boolean; ipRestriction: boolean; lastAudit: string; };
  cloudStorage: { provider: string; isConnected: boolean; rootFolder: string; adminEmail: string; };
}

// --- Helpers ---
const callGemini = async (prompt: string, systemInstruction: string) => {
  const apiKey = ""; 
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;
  try {
    const response = await fetch(url, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], systemInstruction: { parts: [{ text: systemInstruction }] } })
    });
    if (!response.ok) throw new Error(`Gemini API Error: ${response.statusText}`);
    const data = await response.json();
    return data.candidates?.[0]?.content?.parts?.[0]?.text || "I apologize, I couldn't generate a response at this time.";
  } catch (error) { console.error("AI Error:", error); return "System Error: Unable to contact AI service."; }
};

const sanitizeInput = (input: string) => input.replace(/[<>]/g, '');
const validatePassword = (password: string) => {
  if (password.length < 8) return "Password must be at least 8 characters long.";
  if (!/[A-Z]/.test(password)) return "Password must contain at least one uppercase letter.";
  if (!/\d/.test(password)) return "Password must contain at least one number.";
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) return "Password must contain at least one special character.";
  return null;
};
const logSecurityEvent = async (event: string, userEmail: string, details: string) => {
  console.log(`[AUDIT LOG] ${new Date().toISOString()} | ${event} | ${userEmail} | ${details}`);
};

// --- COMPONENTS (Defined in Order) ---

const AIAssistant = ({ config }: { config: FirmConfig }) => {
  const [messages, setMessages] = useState<{role: 'user' | 'model', text: string}[]>([
    { role: 'model', text: `Hello. I am the Sterling & Stone automated tax assistant. How can I help you with general tax inquiries today?` }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => { if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight; }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMsg = input; setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]); setLoading(true);
    const systemPrompt = `You are a helpful, professional tax assistant for a high-end CPA firm called "${config.name}". Your tone is formal, precise, and polite.`;
    const response = await callGemini(userMsg, systemPrompt);
    setMessages(prev => [...prev, { role: 'model', text: response }]); setLoading(false);
  };

  return (
    <div className="flex flex-col h-[500px] bg-white border border-slate-200 rounded-sm shadow-sm">
      <div className="p-4 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
        <div className="flex items-center gap-2 text-slate-800 font-medium"><Sparkles className="text-amber-500" size={18} /> Sterling AI Assistant</div>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4" ref={scrollRef}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-lg text-sm leading-relaxed ${msg.role === 'user' ? 'bg-slate-900 text-white rounded-br-none' : 'bg-slate-100 text-slate-800 rounded-bl-none border border-slate-200'}`}>{msg.text}</div>
          </div>
        ))}
        {loading && <div className="text-xs text-slate-400 ml-4">Thinking...</div>}
      </div>
      <div className="p-4 border-t border-slate-200 bg-slate-50 flex gap-2">
        <input type="text" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleSend()} placeholder="Ask a question..." className="flex-1 border border-slate-300 rounded-sm px-3 py-2 text-sm focus:outline-none focus:border-amber-500" disabled={loading} />
        <button onClick={handleSend} disabled={loading} className="bg-amber-600 hover:bg-amber-700 text-white p-2 rounded-sm"><Send size={18} /></button>
      </div>
    </div>
  );
};

const AdminEmailDrafter = ({ config }: { config: FirmConfig }) => {
  const [topic, setTopic] = useState('');
  const [tone, setTone] = useState('Professional & Polite');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!topic) return; setLoading(true);
    const response = await callGemini(`Topic: ${topic}\nTone: ${tone}`, `You are an executive assistant for "${config.principal}". Draft a client email.`);
    setResult(response); setLoading(false);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div className="space-y-6">
        <textarea className="w-full border border-slate-300 rounded-sm p-3 text-sm h-32" placeholder="Email topic..." value={topic} onChange={(e) => setTopic(e.target.value)} />
        <select className="w-full border border-slate-300 rounded-sm p-3 text-sm" value={tone} onChange={(e) => setTone(e.target.value)}><option>Professional & Polite</option><option>Urgent</option></select>
        <button onClick={handleGenerate} disabled={loading || !topic} className="w-full bg-slate-900 text-white py-3 rounded-sm text-sm font-bold flex justify-center gap-2">{loading ? <Sparkles className="animate-spin" /> : <Sparkles />} Draft Email</button>
      </div>
      <div className="bg-slate-50 border border-slate-200 rounded-sm p-6 relative min-h-[200px]">
        {result ? <div className="prose prose-sm max-w-none whitespace-pre-wrap text-slate-700 text-sm font-serif">{result}</div> : <div className="text-slate-400 text-sm text-center mt-10">AI output will appear here...</div>}
      </div>
    </div>
  );
};

const Navigation = ({ currentView, setView, user, onLogout, config }: { currentView: ViewState, setView: (v: ViewState) => void, user: any, onLogout: () => void, config: FirmConfig }) => {
  const [isOpen, setIsOpen] = useState(false);
  const isVerifiedUser = user && !user.isAnonymous;
  const isAdmin = isVerifiedUser && user?.email === MASTER_ADMIN_EMAIL;
  const NavItem = ({ view, label }: { view: ViewState, label: string }) => (
    <button onClick={() => { setView(view); setIsOpen(false); }} className={`text-sm font-medium tracking-wide transition-colors ${currentView === view ? 'text-amber-500' : 'text-slate-300 hover:text-white'}`}>{label}</button>
  );
  return (
    <nav className="bg-slate-950 border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-20">
          <div className="flex items-center cursor-pointer" onClick={() => setView('home')}>
            <Shield className="h-8 w-8 text-amber-500 mr-3" />
            <div><h1 className="text-xl font-serif text-white tracking-wider uppercase">{config.name}</h1><p className="text-xs text-slate-400 tracking-widest">EST. 1998</p></div>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <NavItem view="home" label="HOME" />
            <NavItem view="services" label="EXPERTISE" />
            <NavItem view="about" label="THE FIRM" />
            <NavItem view="contact" label="CONTACT" />
            {isVerifiedUser ? (
              <div className="flex items-center gap-4 ml-4">
                <button onClick={() => setView(isAdmin ? 'admin' : 'portal')} className="text-white text-sm hover:text-amber-500 flex items-center gap-2">{isAdmin ? <Settings size={16} /> : <User size={16} />} {isAdmin ? 'Admin' : 'Portal'}</button>
                <button onClick={onLogout} className="text-slate-400 hover:text-white"><LogOut size={18} /></button>
              </div>
            ) : (
              <button onClick={() => setView('portal')} className="bg-amber-600 hover:bg-amber-700 text-white px-6 py-2 rounded-sm text-sm font-medium tracking-wide flex items-center gap-2"><Lock size={14} /> CLIENT LOGIN</button>
            )}
          </div>
          <div className="flex items-center md:hidden"><button onClick={() => setIsOpen(!isOpen)} className="text-slate-300">{isOpen ? <X /> : <Menu />}</button></div>
        </div>
      </div>
      {isOpen && <div className="md:hidden bg-slate-900 border-b border-slate-800 p-4 space-y-2 flex flex-col"><NavItem view="home" label="Home" /><NavItem view="services" label="Expertise" /><NavItem view="portal" label="Client Portal" /></div>}
    </nav>
  );
};

const Hero = ({ setView, config }: { setView: (v: ViewState) => void, config: FirmConfig }) => (
  <div className="relative bg-slate-900 overflow-hidden py-32 md:py-48">
    <div className="absolute inset-0 bg-gradient-to-r from-slate-950 via-slate-900 to-transparent z-10"></div>
    <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="md:w-2/3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-amber-500/30 bg-amber-500/10 text-amber-500 text-xs tracking-widest font-bold mb-6">PREMIER TAX ADVISORY</div>
        <h1 className="text-4xl md:text-6xl font-serif text-white leading-tight mb-6">Protecting Wealth Across <br/><span className="text-amber-500">Borders & Generations.</span></h1>
        <p className="text-lg text-slate-300 mb-10 max-w-2xl font-light leading-relaxed">{config.tagline}.</p>
        <div className="flex flex-col sm:flex-row gap-4">
          <button onClick={() => setView('contact')} className="bg-amber-600 hover:bg-amber-700 text-white px-8 py-4 rounded-sm text-sm font-bold tracking-widest">SCHEDULE CONSULTATION</button>
          <button onClick={() => setView('services')} className="border border-slate-600 hover:border-white text-white px-8 py-4 rounded-sm text-sm font-bold tracking-widest">EXPLORE SERVICES</button>
        </div>
      </div>
    </div>
  </div>
);

const Services = () => (
  <div className="bg-white py-24">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-16"><h2 className="text-3xl font-serif text-slate-900 mb-4">Our Expertise</h2><div className="w-24 h-1 bg-amber-500 mx-auto"></div></div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {[
          { title: "International Tax", icon: <Globe className="h-8 w-8 text-amber-500" />, desc: "FBAR, FATCA, and cross-border income." },
          { title: "Strategic Planning", icon: <TrendingUp className="h-8 w-8 text-amber-500" />, desc: "Proactive liability minimization." },
          { title: "Trust & Estate", icon: <Shield className="h-8 w-8 text-amber-500" />, desc: "Wealth transfer structures." }
        ].map((s, i) => (
          <div key={i} className="group p-8 bg-slate-50 border border-slate-100 hover:bg-slate-900 transition-colors">
            <div className="mb-6 p-3 bg-white w-fit shadow-sm">{s.icon}</div>
            <h3 className="text-xl font-semibold text-slate-900 mb-3 group-hover:text-white">{s.title}</h3>
            <p className="text-slate-600 group-hover:text-slate-400 text-sm">{s.desc}</p>
          </div>
        ))}
      </div>
    </div>
  </div>
);

const Contact = ({ config }: { config: FirmConfig }) => (
  <div className="bg-slate-50 py-24">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
        <div>
          <h2 className="text-3xl font-serif text-slate-900 mb-6">Private Consultation</h2>
          <div className="space-y-6">
            <div className="flex items-start"><MapPin className="h-6 w-6 text-amber-600 mr-4" /><div><h4 className="text-sm font-bold text-slate-900">Headquarters</h4><p className="text-slate-600">{config.address}</p></div></div>
            <div className="flex items-start"><Phone className="h-6 w-6 text-amber-600 mr-4" /><div><h4 className="text-sm font-bold text-slate-900">Direct Line</h4><p className="text-slate-600">{config.phone}</p></div></div>
            <div className="flex items-start"><Mail className="h-6 w-6 text-amber-600 mr-4" /><div><h4 className="text-sm font-bold text-slate-900">Email</h4><p className="text-slate-600">{config.email}</p></div></div>
          </div>
        </div>
        <div className="bg-white p-8 shadow-lg border-t-4 border-amber-500">
          <form className="space-y-6">
            <div><label className="block text-sm font-medium text-slate-700">Email</label><input type="email" className="mt-1 block w-full border-slate-300 p-3 border" /></div>
            <div><label className="block text-sm font-medium text-slate-700">Message</label><textarea rows={4} className="mt-1 block w-full border-slate-300 p-3 border"></textarea></div>
            <button className="w-full bg-slate-900 text-white py-3 font-medium">SEND SECURE MESSAGE</button>
          </form>
        </div>
      </div>
    </div>
  </div>
);

const About = ({ config }: { config: FirmConfig }) => (
  <div className="bg-white py-24">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h2 className="text-base text-amber-600 font-semibold tracking-wide uppercase">The Principal</h2>
      <p className="mt-2 text-3xl leading-8 font-extrabold text-slate-900 sm:text-4xl font-serif">{config.principal}</p>
      <p className="mt-4 max-w-2xl mx-auto text-xl text-slate-500">Twenty years of navigating complex tax codes for the world's most demanding clients.</p>
    </div>
  </div>
);

const AdminDashboard = ({ user, config, allowedClients: initialClients }: { user: any, config: FirmConfig, allowedClients: string[] }) => {
  const [activeTab, setActiveTab] = useState('access');
  const [newClientEmail, setNewClientEmail] = useState('');
  const [allowedClients, setAllowedClients] = useState<string[]>(initialClients);
  const [editConfig, setEditConfig] = useState<FirmConfig>(config);
  const [saving, setSaving] = useState(false);

  useEffect(() => setAllowedClients(initialClients), [initialClients]);

  const handleAddClient = async (e: React.FormEvent) => {
    e.preventDefault(); if (!newClientEmail) return;
    const email = sanitizeInput(newClientEmail);
    const updatedList = [...allowedClients, email];
    setAllowedClients(updatedList); setNewClientEmail(''); // Immediate UI update
    
    if (user.uid.startsWith('demo-')) {
      alert(`(Demo) ${email} added to allowlist.`); return;
    }
    try {
      await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'access', 'whitelist'), { emails: updatedList });
      alert(`Success: ${email} added.`);
    } catch (error) { console.error(error); }
  };

  const handleSaveSettings = async (e: React.FormEvent) => {
    e.preventDefault(); setSaving(true);
    if (user.uid.startsWith('demo-')) {
      setTimeout(() => { setSaving(false); alert("Settings saved (Demo Mode)"); }, 1000); return;
    }
    try {
      await setDoc(doc(db, 'artifacts', appId, 'public', 'data', 'settings', 'firm_config'), editConfig);
      alert("Settings saved!");
    } catch (error) { console.error(error); } finally { setSaving(false); }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between mb-8">
          <h1 className="text-3xl font-serif text-slate-900">Firm Administration</h1>
          <div className="bg-slate-900 text-white px-4 py-1 rounded-full text-xs font-bold flex items-center gap-2"><Settings size={12} /> MASTER ADMIN</div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1 space-y-2">
            {['access', 'communication', 'security', 'storage', 'settings'].map(tab => (
              <button key={tab} onClick={() => setActiveTab(tab)} className={`w-full text-left px-4 py-3 rounded-sm text-sm font-medium capitalize ${activeTab === tab ? 'bg-slate-900 text-white' : 'bg-white text-slate-600'}`}>{tab}</button>
            ))}
          </div>
          <div className="lg:col-span-3">
            {activeTab === 'access' && (
              <div className="bg-white shadow-lg rounded-sm p-6 border border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Manage Client Access</h3>
                <form onSubmit={handleAddClient} className="flex gap-4 mb-8">
                  <input type="email" placeholder="Client email..." value={newClientEmail} onChange={(e) => setNewClientEmail(e.target.value)} className="flex-1 px-4 py-2 border border-slate-300" />
                  <button className="bg-slate-900 text-white px-4 py-2 font-bold flex items-center gap-2"><Plus size={16} /> Add</button>
                </form>
                <div className="bg-slate-50 border border-slate-200 rounded-sm">
                  {allowedClients.map((email, idx) => (
                    <div key={idx} className="px-6 py-3 border-b flex justify-between text-sm font-medium text-slate-900">
                      {email} <button className="text-red-600"><Trash2 size={14} /></button>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {activeTab === 'communication' && <div className="bg-white shadow-lg rounded-sm p-6"><h3 className="font-bold mb-4">Communication</h3><AdminEmailDrafter config={config} /></div>}
            {activeTab === 'settings' && (
              <div className="bg-white shadow-lg rounded-sm p-6">
                <h3 className="font-bold mb-4">Website Settings</h3>
                <form onSubmit={handleSaveSettings} className="space-y-4">
                  <input className="w-full border p-2" value={editConfig.name} onChange={e => setEditConfig({...editConfig, name: e.target.value})} placeholder="Firm Name" />
                  <button disabled={saving} className="bg-amber-600 text-white px-4 py-2">{saving ? 'Saving...' : 'Save'}</button>
                </form>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const Portal = ({ user, config, allowedClients, onManualLogin }: { user: any, config: FirmConfig, allowedClients: string[], onManualLogin: (email: string) => void }) => {
  const [authMode, setAuthMode] = useState<AuthMode>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('docs');

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      if (auth.currentUser?.isAnonymous) await signOut(auth);
      if (authMode === 'login') {
        if (!allowedClients.includes(email) && email !== MASTER_ADMIN_EMAIL) throw new Error("Access Denied");
        await signInWithEmailAndPassword(auth, email, password);
      } else {
        await createUserWithEmailAndPassword(auth, email, password);
      }
    } catch (err: any) {
      if (err.code === 'auth/operation-not-allowed' || err.code === 'auth/user-not-found') { onManualLogin(email); return; }
      setError(err.message);
    } finally { setLoading(false); }
  };

  if (!user || user.isAnonymous) {
    return (
      <div className="min-h-[80vh] bg-slate-100 flex items-center justify-center py-12 px-4">
        <div className="max-w-md w-full bg-white p-10 shadow-2xl border-t-4 border-amber-500">
          <h2 className="text-3xl font-serif font-bold text-center text-slate-900 mb-6">Secure Portal</h2>
          <form onSubmit={handleAuth} className="space-y-6">
            <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} className="w-full border p-3" placeholder="Email" />
            <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} className="w-full border p-3" placeholder="Password" />
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <button disabled={loading} className="w-full bg-slate-900 text-white py-3 font-medium">{loading ? 'Processing...' : 'Access Vault'}</button>
            <div className="text-center text-xs text-amber-600 cursor-pointer" onClick={() => setEmail('client@example.com') || setPassword('Client@1234')}>Demo Credentials</div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-serif text-slate-900">Client Vault</h1>
          <div className="flex bg-slate-200 rounded p-1">
            <button onClick={() => setActiveTab('docs')} className={`px-4 py-1 text-sm font-medium rounded ${activeTab === 'docs' ? 'bg-white shadow' : ''}`}>Docs</button>
            <button onClick={() => setActiveTab('ai')} className={`px-4 py-1 text-sm font-medium rounded ${activeTab === 'ai' ? 'bg-white shadow' : ''}`}>AI Assistant</button>
          </div>
        </div>
        {activeTab === 'docs' ? (
          <div className="bg-white shadow-xl rounded-sm p-12 text-center text-slate-400">
            <FileCheck className="h-12 w-12 mx-auto mb-3 opacity-50" />
            <p>No documents found. Secure upload is ready.</p>
          </div>
        ) : <AIAssistant config={config} />}
      </div>
    </div>
  );
};

const Footer = ({ setView, config }: { setView: (v: ViewState) => void, config: FirmConfig }) => (
  <footer className="bg-slate-950 text-slate-400 py-12 border-t border-slate-900 text-center text-xs">
    <p>&copy; {new Date().getFullYear()} {config.name}. Secured by 256-bit SSL.</p>
  </footer>
);

// --- MAIN APP ---
export default function App() {
  const [view, setView] = useState<ViewState>('home');
  const [user, setUser] = useState<any>(null);
  const [config, setConfig] = useState<FirmConfig>(DEFAULT_CONFIG);
  const [allowedClients, setAllowedClients] = useState<string[]>(DEFAULT_ALLOWED_CLIENTS);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) await signInWithCustomToken(auth, __initial_auth_token);
      else await signInAnonymously(auth);
    };
    init();
    return onAuthStateChanged(auth, setUser);
  }, []);

  useEffect(() => {
    // 🛑 CRITICAL FIX: Do not attach database listeners if user is not logged in or is anonymous.
    // This prevents "Permission Denied" errors for guests.
    if (!user || user.isAnonymous) {
      setLoading(false);
      return; 
    }

    const unsubConfig = onSnapshot(doc(db, 'artifacts', appId, 'public', 'data', 'settings', 'firm_config'), 
      (s) => { if (s.exists()) setConfig(s.data() as FirmConfig); setLoading(false); },
      (e) => { console.warn("Using default config (Offline Mode)"); setLoading(false); }
    );
    const unsubClients = onSnapshot(doc(db, 'artifacts', appId, 'public', 'data', 'access', 'whitelist'),
      (s) => { if (s.exists()) setAllowedClients(s.data().emails || []); },
      (e) => console.warn("Using default client list")
    );
    return () => { unsubConfig(); unsubClients(); };
  }, [user?.uid]);

  const handleManualLogin = (email: string) => setUser({ uid: 'demo-' + Date.now(), email, isAnonymous: false });
  const handleLogout = async () => { await signOut(auth); await signInAnonymously(auth); setView('home'); };
  const isAdmin = user?.email === MASTER_ADMIN_EMAIL;

  if (loading) return <div className="h-screen flex items-center justify-center">Secure Loading...</div>;

  return (
    <div className="min-h-screen font-sans text-slate-900 bg-white">
      <Navigation currentView={view} setView={setView} user={user} onLogout={handleLogout} config={config} />
      {view === 'home' && <><Hero setView={setView} config={config} /><Services /><About config={config} /><Contact config={config} /></>}
      {view === 'services' && <Services />}
      {view === 'about' && <About config={config} />}
      {view === 'contact' && <Contact config={config} />}
      {view === 'portal' && <Portal user={user} config={config} allowedClients={allowedClients} onManualLogin={handleManualLogin} />}
      {view === 'admin' && (isAdmin ? <AdminDashboard user={user} config={config} allowedClients={allowedClients} /> : <div className="p-12 text-center">Access Restricted</div>)}
      <Footer setView={setView} config={config} />
    </div>
  );
}
