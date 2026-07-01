function ShiftCards() {
  const shifts = [
    {
      title: "Mañana",
      time: "10:00 — 13:00",
    },
    {
      title: "Mediodía",
      time: "14:00 — 17:00",
    },
    {
      title: "Tarde",
      time: "18:00 — 21:00",
    },
  ];

  return (
    <section className="py-24 px-6 bg-[#DCCFC0]">
      <div className="max-w-6xl mx-auto">
        
        <div className="text-center mb-16">
          <p className="text-[#C8A96B] uppercase tracking-[4px] mb-4">
            Turnos
          </p>

          <h2 className="text-5xl font-serif text-[#2D2D2D]">
            Elegí el horario ideal
          </h2>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {shifts.map((shift, index) => (
            <div
              key={index}
              className="
                bg-[#F3ECE4]
                rounded-3xl
                p-10
                text-center
                shadow-[0_10px_30px_rgba(0,0,0,0.05)]
                hover:scale-[1.02]
                transition-all
                duration-300
              "
            >
              <h3 className="text-3xl font-serif text-[#2D2D2D] mb-4">
                {shift.title}
              </h3>

              <p className="text-lg text-[#2D2D2D]/70">
                {shift.time}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default ShiftCards;