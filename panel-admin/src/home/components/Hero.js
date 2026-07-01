function Hero() {
  return (
    <section className="px-6 py-20 bg-[#DCCFC0]">
      <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-16 items-center">
        
        <div>
          <p className="text-[#C8A96B] uppercase tracking-[4px] mb-4">
            Eventos únicos
          </p>

          <h2 className="text-6xl leading-tight text-[#2D2D2D] font-serif mb-8">
            El espacio perfecto para celebrar momentos inolvidables
          </h2>

          <p className="text-[#2D2D2D]/70 text-lg leading-relaxed mb-10">
            Un salón cálido, elegante y pensado para que chicos y grandes
            disfruten una experiencia especial.
          </p>

          <a
            href="https://wa.me/5490000000000"
            target="_blank"
            rel="noreferrer"
            className="
              inline-block
              bg-[#7E9485]
              hover:bg-[#5F7468]
              text-white
              px-8
              py-4
              rounded-full
              text-lg
              transition-all
              duration-300
            "
          >
            Consultanos por WhatsApp
          </a>
        </div>

        <div>
          <div
            className="
              w-full
              h-[600px]
              bg-[#F3ECE4]
              rounded-[40px]
              shadow-[0_10px_30px_rgba(0,0,0,0.06)]
            "
          >
          </div>
        </div>

      </div>
    </section>
  );
}

export default Hero;