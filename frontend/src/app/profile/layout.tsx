import { Header } from '@/components/header'

export default function ProfileLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-slate-50">
      <Header />
      <main>{children}</main>
    </div>
  )
}
