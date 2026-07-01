function Features() {
  const features = [
    "Hasta 40 niños",
    "Pelotero incluido",
    "Cocina equipada",
    "Mesas y sillas",
    "Ambiente climatizado",
    "Espacio cómodo y seguro",
  ];

  return (
    <section className="py-24 px-6 bg-[#F3ECE4]">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-[#C8A96B] uppercase tracking-[4px] mb-4">
            Nuestro espacio
          </p>

          <h2 className="text-5xl text-[#2D2D2D] font-serif mb-6">
            Todo lo necesario para un evento inolvidable
          </h2>

          <p className="text-[#2D2D2D]/70 max-w-2xl mx-auto">
            Un salón cálido, moderno y pensado para que chicos y grandes
            disfruten cada momento.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((item, index) => (
            <div
              key={index}
              className="
                bg-[#DCCFC0]
                rounded-3xl
                p-8
                shadow-[0_10px_30px_rgba(0,0,0,0.05)]
                hover:scale-[1.02]
                transition-all
                duration-300
              "
            >
              <h3 className="text-2xl text-[#2D2D2D] font-serif mb-4">
                ✦
              </h3>

              <p className="text-[#2D2D2D] text-lg">
                {item}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default Features;