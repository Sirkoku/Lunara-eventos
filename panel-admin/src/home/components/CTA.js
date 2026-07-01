function CTA() {
  return (
    <section className="py-24 px-6 bg-[#7E9485]">
      <div className="max-w-4xl mx-auto text-center">
        <p className="text-[#F3ECE4] uppercase tracking-[4px] mb-4">
          Reservá tu fecha
        </p>

        <h2 className="text-5xl font-serif text-white mb-6">
          ¿Querés consultar disponibilidad?
        </h2>

        <p className="text-white/80 text-lg mb-10 max-w-2xl mx-auto">
          Escribinos por WhatsApp y te ayudamos a organizar un cumpleaños
          inolvidable.
        </p>

        <a
          href="https://wa.me/5490000000000"
          target="_blank"
          rel="noreferrer"
          className="
            inline-block
            bg-[#F3ECE4]
            text-[#2D2D2D]
            px-10
            py-4
            rounded-full
            text-lg
            hover:scale-105
            transition-all
            duration-300
          "
        >
          Consultanos
        </a>
      </div>
    </section>
  );
}

export default CTA;