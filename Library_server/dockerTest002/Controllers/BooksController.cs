using dockerTest002.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace dockerTest002.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BooksController : ControllerBase
    {
        private readonly ConfConnDB _confConnDb;

        public BooksController(ConfConnDB confConnDb)
        {
            _confConnDb = confConnDb;
        }

        // GET: api/Books
        [HttpGet("all")]
        public async Task<ActionResult<IEnumerable<Ksiazka>>> GetBooks()
        {
            return await _confConnDb.Ksiazka.ToListAsync();
        }

        // GET: api/Books/{id}
        // GET: api/Books/0?title=...
        // GET: api/Books/0?author=...
        [HttpGet("{id}")]
        public async Task<ActionResult> GetItem(int id, bool? av, string title = null, string author = null, string genre = null)
        {
            if (id > 0)
            {
                var bookById = await _confConnDb.Ksiazka.FindAsync(id);

                if (bookById == null)
                {
                    return NotFound();
                }

                return Ok(bookById);
            }

            IQueryable<Ksiazka> query = _confConnDb.Ksiazka;

            if (!string.IsNullOrEmpty(title))
            {
                query = query.Where(b => b.Tytul.Contains(title));
            }

            if (!string.IsNullOrEmpty(author))
            {
                query = query.Where(b => b.Autor.Contains(author));
            }

            if (!string.IsNullOrEmpty(genre))
            {
                query = query.Where(b => b.Gatunek.Contains(genre));
            }

            if (av.HasValue)
            {
                query = query.Where(b => b.Dostepnosc.Equals(av));
            }

            var books = await query.ToListAsync();

            if (books.Count == 0)
            {
                return NotFound();
            }

            return Ok(books);
        }

        // POST: api/Books
        [Authorize]
        [HttpPost]
        public async Task<ActionResult<Ksiazka>> PostBook(Ksiazka book)
        {
            _confConnDb.Ksiazka.Add(book);
            await _confConnDb.SaveChangesAsync();

            return CreatedAtAction("GetItem", new { id = book.KsiazkaID }, book);
        }

        // PUT: api/Books/put
        [Authorize]
        [HttpPut("put")]
        public async Task<IActionResult> PutBook(Ksiazka book)
        {
            var existingBook = await _confConnDb.Ksiazka.FindAsync(book.KsiazkaID);
            if (existingBook == null)
            {
                return NotFound();
            }

            existingBook.Tytul = book.Tytul;
            existingBook.Autor = book.Autor;
            existingBook.Dostepnosc = book.Dostepnosc;
            existingBook.Gatunek = book.Gatunek;
            existingBook.DataWydania = book.DataWydania;
            existingBook.LiczbaStron = book.LiczbaStron;

            await _confConnDb.SaveChangesAsync();

            return NoContent();
        }

        // DELETE: api/Books/5
        [Authorize]
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteBook(int id)
        {
            var book = await _confConnDb.Ksiazka.FindAsync(id);
            if (book == null)
            {
                return NotFound();
            }

            _confConnDb.Ksiazka.Remove(book);
            await _confConnDb.SaveChangesAsync();

            return NoContent();
        }
    }
}
