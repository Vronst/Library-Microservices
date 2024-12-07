namespace dockerTest002.Models
{
    public class Ksiazka
    {
        public int KsiazkaID { get; set; }
        public string Tytul { get; set; }
        public string Autor { get; set; }
        public bool Dostepnosc { get; set; }
        public string Gatunek { get; set; }
        public DateOnly DataWydania { get; set; }
        public int LiczbaStron { get; set; }

    }
}
