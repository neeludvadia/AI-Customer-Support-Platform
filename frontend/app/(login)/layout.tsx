
export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <div className="min-w-screen h-screen bg-white text-black">{children}</div>
    );
}