/***********************************************************************/
/*Random Quote Generator using https://type.fit/api/quotes             */
/***********************************************************************/

const quoteText = document.getElementById('quote');
const authorText = document.getElementById('author');
//Limit on number of quotes
const QUOTE_ARRAY_MAX = 1643;

//Return a random number up to the QUOTE_ARRAY_MAX
function getRandomQuote() {
    return Math.floor(Math.random() * (QUOTE_ARRAY_MAX + 1));
}

//Asynchronous fetch function
async function getQuote() {
    const apiUrl = 'https://type.fit/api/quotes';
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        let randomQuote = getRandomQuote();
        //If author is blank, add 'Unknown'
        if (data[randomQuote].author === null) {
            authorText.innerText = 'Unknown';
        } else {
            authorText.innerText = data[randomQuote].author;
        }
        //Reduce font size for long quotes by assigning classList('long-quote)
        if (data[randomQuote].text.length > 120) {
            quoteText.classList.add('long-quote');
        } else {
            quoteText.classList.remove('long-quote');
        }
        quoteText.innerText = data[randomQuote].text;
    } catch (error) {
        console.log('Error', error);
    }
}

//On Load
getQuote();