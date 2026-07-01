function Header() {
return (
    <header className="w-full px-6 py-6 bg-[#DCCFC0]">
    <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        <div>
        <h1 className="text-3xl font-serif text-[#2D2D2D]">
            Lunara
        </h1>

        <p className="text-sm text-[#2D2D2D]/70 mt-1">
            Salón de eventos infantiles
        </p>
        </div>

        <a
        href="https://wa.me/5490000000000"
        target="_blank"
        rel="noreferrer"
        className="
            bg-[#7E9485]
            hover:bg-[#5F7468]
            text-white
            px-6
            py-3
            rounded-full
            transition-all
            duration-300
        "
        >
        Consultanos
        </a>
    </div>
    </header>
);
}

export default Header;