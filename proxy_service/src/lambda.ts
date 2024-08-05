import axios from 'axios';

export const handler = async (event: any, context: any) => {
  const urlToFetch = event.queryStringParameters.url;

  try {
    const response = await axios.get(urlToFetch);
    return {
      statusCode: 200,
      body: JSON.stringify({
        content: response.data,
      }),
      headers: {
        'Content-Type': 'application/json',
      },
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: error,
      }),
    };
  }
};
