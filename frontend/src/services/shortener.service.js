export const ShortenerService = {
    async getShortLink(longLink) {

    try {
        const response = await fetch(process.env.REACT_APP_API_URL, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ target_url: longLink }),
        });
        const data = await response.json();
        const shortLink = data.url;

        return shortLink;

        } catch (error) {
            console.error('Error', error);
            return '';
        }
    }
}
