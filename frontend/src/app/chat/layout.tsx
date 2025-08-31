import { Header } from '@/components/header'

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="h-screen bg-slate-50 flex flex-col">
      <Header />
      <div className="flex-1 overflow-hidden">{children}</div>
    </div>
  )
}
