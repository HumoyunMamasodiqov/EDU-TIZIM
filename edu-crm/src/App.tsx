import { useState } from 'react'
import {
  LayoutDashboard, ClipboardList, Users, Layers, UserCheck, Trophy,
  BookOpen, Coins, Shield, Settings, TrendingUp, FileText, ShoppingCart,
  Search, Bell, Mail, ChevronDown, Globe, Upload, Plus,
  MoreHorizontal, UserPlus, Archive, Download, Import, GraduationCap,
  Menu
} from 'lucide-react'

const sidebarItems = [
  { icon: LayoutDashboard, label: 'Dashboard', active: false },
  { icon: ClipboardList, label: 'Topshiriqlar', active: false },
  { icon: Users, label: 'Lidlar', active: false },
  { icon: Layers, label: 'Guruh', active: true },
  { icon: UserCheck, label: "O'quvchilar", active: false },
  { icon: Trophy, label: 'Gamifikatsiya', active: false },
  { icon: BookOpen, label: "O'quv bo'limi", active: false },
  { icon: Coins, label: 'Moliya', active: false },
  { icon: Shield, label: 'Nazorat', active: false },
  { icon: Settings, label: 'Boshqaruv', active: false },
  { icon: TrendingUp, label: 'Sotuv va marketing', active: false },
  { icon: FileText, label: 'Hisobotlar', active: false },
  { icon: ShoppingCart, label: 'Sozlamalar', active: false },
]

const students = [
  { id: 1, name: 'Aliyev Bekzod', date: '12.03.2026', phone: '+998 90 123 45 67', balance: '0', price: '500 000', coin: '1 200' },
  { id: 2, name: 'Karimova Sevara', date: '14.03.2026', phone: '+998 91 234 56 78', balance: '50 000', price: '450 000', coin: '980' },
  { id: 3, name: 'Nazarov Jahongir', date: '15.03.2026', phone: '+998 93 345 67 89', balance: '0', price: '550 000', coin: '2 100' },
  { id: 4, name: 'Rahimova Dilnoza', date: '18.03.2026', phone: '+998 94 456 78 90', balance: '120 000', price: '500 000', coin: '1 500' },
  { id: 5, name: 'Sultonov Ozod', date: '20.03.2026', phone: '+998 95 567 89 01', balance: '0', price: '400 000', coin: '850' },
  { id: 6, name: 'Xasanova Malika', date: '22.03.2026', phone: '+998 96 678 90 12', balance: '75 000', price: '520 000', coin: '1 780' },
  { id: 7, name: 'Toshmatov Elmurod', date: '25.03.2026', phone: '+998 97 789 01 23', balance: '0', price: '480 000', coin: '650' },
  { id: 8, name: 'Abdullayev Kamron', date: '27.03.2026', phone: '+998 98 890 12 34', balance: '200 000', price: '600 000', coin: '3 200' },
  { id: 9, name: 'Jo\'rayev Aziz', date: '29.03.2026', phone: '+998 99 901 23 45', balance: '30 000', price: '470 000', coin: '1 100' },
  { id: 10, name: 'Nosirova Zarnigor', date: '01.04.2026', phone: '+998 90 012 34 56', balance: '0', price: '530 000', coin: '2 050' },
  { id: 11, name: 'Erkinov Sanjar', date: '03.04.2026', phone: '+998 91 123 45 67', balance: '90 000', price: '490 000', coin: '1 400' },
  { id: 12, name: 'Komilova Mohichehra', date: '05.04.2026', phone: '+998 93 234 56 78', balance: '0', price: '510 000', coin: '1 900' },
]

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [selectAll, setSelectAll] = useState(false)
  const [selectedIds, setSelectedIds] = useState<number[]>([])

  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedIds([])
    } else {
      setSelectedIds(students.map(s => s.id))
    }
    setSelectAll(!selectAll)
  }

  const handleSelect = (id: number) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter(i => i !== id))
    } else {
      setSelectedIds([...selectedIds, id])
    }
  }

  return (
    <div className="min-h-screen bg-[#f8fafc]">
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <aside className={`
          fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 
          transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-auto
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
          flex flex-col
        `}>
          <div className="h-16 flex items-center gap-3 px-5 border-b border-gray-100">
            <div className="w-9 h-9 rounded-lg bg-[#2563eb] flex items-center justify-center">
              <GraduationCap className="text-white" size={18} />
            </div>
            <span className="text-lg font-bold tracking-tight">
              <span className="text-gray-900">Edu</span>
              <span className="text-[#2563eb]">CRM</span>
            </span>
          </div>
          <nav className="flex-1 overflow-y-auto py-3 px-3">
            {sidebarItems.map((item, idx) => (
              <a
                key={idx}
                href="#"
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 mb-0.5 ${
                  item.active
                    ? 'bg-[#2563eb] text-white shadow-sm'
                    : 'text-gray-500 hover:bg-gray-50 hover:text-gray-700'
                }`}
              >
                <item.icon size={18} strokeWidth={item.active ? 2.5 : 1.8} />
                <span>{item.label}</span>
              </a>
            ))}
          </nav>
          <div className="p-3 border-t border-gray-100">
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-500 hover:bg-gray-50 hover:text-gray-700 transition-all"
            >
              <LogOut size={18} strokeWidth={1.8} />
              <span>Chiqish</span>
            </a>
          </div>
        </aside>

        {/* Overlay */}
        {sidebarOpen && (
          <div className="fixed inset-0 bg-black/20 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />
        )}

        {/* Main */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Header */}
          <header className="h-16 bg-white border-b border-gray-200 flex items-center px-4 lg:px-6 gap-4 shrink-0">
            <button className="lg:hidden p-2 -ml-2 rounded-lg hover:bg-gray-50" onClick={() => setSidebarOpen(true)}>
              <Menu size={20} className="text-gray-500" />
            </button>

            <div className="flex items-center gap-3 min-w-0">
              <div className="flex items-center gap-2 bg-gray-50 px-3.5 py-1.5 rounded-lg border border-gray-200 cursor-pointer hover:border-gray-300 transition-colors shrink-0">
                <GraduationCap size={16} className="text-[#2563eb]" />
                <span className="text-sm font-medium text-gray-700">IT House Akademiyasi</span>
                <ChevronDown size={14} className="text-gray-400" />
              </div>
            </div>

            <div className="flex-1 max-w-md relative hidden md:block">
              <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Qidirish..."
                className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-[#2563eb] focus:bg-white transition-all"
              />
            </div>

            <div className="flex items-center gap-2 ml-auto">
              <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-gray-50 text-sm text-gray-600">
                <Globe size={15} />
                <span className="font-medium">UZ</span>
              </button>
              <button className="relative p-2 rounded-lg hover:bg-gray-50 text-gray-500">
                <Bell size={18} />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full" />
              </button>
              <button className="relative p-2 rounded-lg hover:bg-gray-50 text-gray-500">
                <Mail size={18} />
              </button>
              <div className="w-8 h-8 rounded-full bg-[#2563eb] text-white flex items-center justify-center text-xs font-bold ml-1">
                A
              </div>
            </div>
          </header>

          {/* Content */}
          <main className="flex-1 overflow-y-auto p-4 lg:p-6">
            {/* Page Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
              <div>
                <h1 className="text-xl lg:text-2xl font-bold text-gray-900">Foundation N1</h1>
                <p className="text-sm text-gray-500 mt-0.5">Guruh profili va talabalar ro'yxati</p>
              </div>
              <div className="flex items-center gap-2">
                <button className="flex items-center gap-2 px-4 py-2 bg-[#2563eb] text-white rounded-lg text-sm font-medium hover:bg-[#1d4ed8] transition-colors shadow-sm">
                  <UserPlus size={16} />
                  O'quvchi qo'shish
                </button>
                <button className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors">
                  <Download size={16} />
                  Import
                </button>
              </div>
            </div>

            {/* Group Info Card */}
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm mb-6 overflow-hidden">
              <div className="p-5 lg:p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-base font-semibold text-gray-900 flex items-center gap-2">
                    <Info size={16} className="text-[#2563eb]" />
                    Guruh ma'lumotlari
                  </h2>
                  <button className="text-sm text-[#2563eb] font-medium hover:underline">Tahrirlash</button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between py-2.5 px-4 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">Nomi</span>
                      <span className="text-sm font-semibold text-gray-900">Foundation N1</span>
                    </div>
                    <div className="flex items-center justify-between py-2.5 px-4 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">Darajasi</span>
                      <span className="text-sm font-semibold text-gray-900">Beginner</span>
                    </div>
                    <div className="flex items-center justify-between py-2.5 px-4 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">Kurs vaqti</span>
                      <span className="text-sm font-semibold text-gray-900">09:00 - 11:00</span>
                    </div>
                    <div className="flex items-center justify-between py-2.5 px-4 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">Turi</span>
                      <span className="text-sm font-semibold">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-[#2563eb]">
                          Offline
                        </span>
                      </span>
                    </div>
                    <div className="flex items-center justify-between py-2.5 px-4 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">Platforma</span>
                      <span className="text-sm font-semibold text-gray-900">-</span>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between py-2.5 px-4 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">Kurs</span>
                      <span className="text-sm font-semibold text-gray-900">Ingliz tili</span>
                    </div>
                    <div className="flex items-center justify-between py-2.5 px-4 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">Kunlar</span>
                      <span className="text-sm font-semibold text-gray-900">Dushanba, Chorshanba, Juma</span>
                    </div>
                    <div className="flex items-center justify-between py-2.5 px-4 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">O'qituvchi</span>
                      <span className="text-sm font-semibold text-gray-900">Sardor Tursunov</span>
                    </div>
                    <div className="flex items-center justify-between py-2.5 px-4 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">Guruh vaqti</span>
                      <span className="text-sm font-semibold text-gray-900">15.03.2026 - 15.07.2026</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Actions Bar */}
            <div className="flex flex-wrap items-center gap-2 mb-4">
              <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors shadow-sm">
                <Users size={16} />
                O'quvchilar
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors shadow-sm">
                <ClipboardList size={16} />
                Topshiriqlar
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors shadow-sm">
                <Import size={16} />
                Import
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors shadow-sm">
                <Download size={16} />
                Export
              </button>
              <div className="ml-auto flex items-center gap-3">
                <button className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900 transition-colors">
                  <Archive size={16} />
                  Arxiv talabalar
                </button>
                <div className="relative">
                  <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Qidirish..."
                    className="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-48 lg:w-56 focus:outline-none focus:border-[#2563eb] transition-colors"
                  />
                </div>
              </div>
            </div>

            {/* Students Table */}
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-100 bg-gray-50/50">
                      <th className="w-10 px-4 py-3.5 text-left">
                        <input
                          type="checkbox"
                          checked={selectAll}
                          onChange={handleSelectAll}
                          className="rounded border-gray-300 text-[#2563eb] focus:ring-[#2563eb] cursor-pointer"
                        />
                      </th>
                      <th className="w-10 px-2 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider">№</th>
                      <th className="px-3 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider text-left">O'quvchi ismi</th>
                      <th className="px-3 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider text-left">Qo'shilgan sanasi</th>
                      <th className="px-3 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider text-left">Telefon raqam</th>
                      <th className="px-3 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Balans</th>
                      <th className="px-3 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Narxi</th>
                      <th className="px-3 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Coin</th>
                      <th className="px-3 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider text-left">Sertifikat</th>
                      <th className="w-20 px-4 py-3.5 text-xs font-semibold text-gray-500 uppercase tracking-wider text-center">Amallar</th>
                    </tr>
                  </thead>
                  <tbody>
                    {students.map((student, idx) => (
                      <tr
                        key={student.id}
                        className={`border-b border-gray-50 transition-colors hover:bg-blue-50/30 group ${
                          selectedIds.includes(student.id) ? 'bg-blue-50/40' : ''
                        }`}
                      >
                        <td className="px-4 py-3">
                          <input
                            type="checkbox"
                            checked={selectedIds.includes(student.id)}
                            onChange={() => handleSelect(student.id)}
                            className="rounded border-gray-300 text-[#2563eb] focus:ring-[#2563eb] cursor-pointer"
                          />
                        </td>
                        <td className="px-2 py-3 text-sm text-gray-500">{String(idx + 1).padStart(2, '0')}</td>
                        <td className="px-3 py-3">
                          <div className="flex items-center gap-2.5">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#2563eb] to-[#1d4ed8] text-white flex items-center justify-center text-xs font-bold shrink-0">
                              {student.name.charAt(0)}
                            </div>
                            <span className="text-sm font-medium text-gray-900">{student.name}</span>
                          </div>
                        </td>
                        <td className="px-3 py-3 text-sm text-gray-600">{student.date}</td>
                        <td className="px-3 py-3 text-sm text-gray-600">{student.phone}</td>
                        <td className="px-3 py-3 text-sm text-right">
                          {student.balance === '0' ? (
                            <span className="text-gray-400">0</span>
                          ) : (
                            <span className="text-green-600 font-medium">{student.balance}</span>
                          )}
                        </td>
                        <td className="px-3 py-3 text-sm text-right font-medium text-gray-900">{student.price}</td>
                        <td className="px-3 py-3 text-sm text-right font-medium text-amber-600">{student.coin}</td>
                        <td className="px-3 py-3">
                          <button className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-[#2563eb] transition-colors px-2 py-1 rounded-md hover:bg-blue-50">
                            <Upload size={14} />
                            <span>Yuklash</span>
                          </button>
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex items-center justify-center gap-0.5">
                            <button className="p-1.5 rounded-md text-gray-400 hover:text-[#2563eb] hover:bg-blue-50 transition-all" title="Yuklash">
                              <Upload size={15} />
                            </button>
                            <button className="p-1.5 rounded-md text-gray-400 hover:text-green-600 hover:bg-green-50 transition-all" title="Qo'shish">
                              <Plus size={15} />
                            </button>
                            <button className="p-1.5 rounded-md text-gray-400 hover:text-[#2563eb] hover:bg-blue-50 transition-all" title="Profil">
                              <UserCheck size={15} />
                            </button>
                            <button className="p-1.5 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-all" title="Ko'proq">
                              <MoreHorizontal size={15} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Table Footer */}
              <div className="flex items-center justify-between px-4 py-3 border-t border-gray-100 bg-gray-50/30">
                <span className="text-xs text-gray-500">
                  {selectedIds.length > 0
                    ? `${selectedIds.length} ta tanlangan`
                    : `${students.length} ta o'quvchi`}
                </span>
                <div className="flex items-center gap-2">
                  <button className="px-3 py-1.5 text-xs font-medium text-gray-500 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">Oldingi</button>
                  <div className="flex items-center gap-1">
                    {[1, 2, 3].map(page => (
                      <button
                        key={page}
                        className={`w-7 h-7 text-xs font-medium rounded-lg transition-colors ${
                          page === 1
                            ? 'bg-[#2563eb] text-white'
                            : 'text-gray-500 hover:bg-gray-100'
                        }`}
                      >
                        {page}
                      </button>
                    ))}
                  </div>
                  <button className="px-3 py-1.5 text-xs font-medium text-gray-500 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">Keyingi</button>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}

function Info(props: any) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <path d="M12 16v-4" />
      <path d="M12 8h.01" />
    </svg>
  )
}

function LogOut(props: any) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
      <polyline points="16 17 21 12 16 7" />
      <line x1="21" x2="9" y1="12" y2="12" />
    </svg>
  )
}

export default App
