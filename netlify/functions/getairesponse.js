const { GoogleGenerativeAI } = require('@google/generative-ai');

exports.handler = async (event, context) => {
  // Handle CORS
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      }
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: {
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { subject, unit, videoTitle, subtitleText, userRawPrompt } = JSON.parse(event.body);

    // Initialize Gemini AI with API key from environment variable
    const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    // Construct the prompt
    let prompt = `教科: ${subject}\n単元: ${unit}\n動画タイトル: ${videoTitle}\n\n`;
    
    if (subtitleText) {
      prompt += `動画の字幕内容:\n${subtitleText}\n\n`;
    }
    
    prompt += `教員からの依頼:\n${userRawPrompt}\n\n`;
    prompt += `上記の情報を基に、教員向けの具体的で実用的な授業支援アイデアを提案してください。`;

    // Generate response
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text })
    };

  } catch (error) {
    console.error('AI Generation Error:', error);
    return {
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        error: `AI応答生成中にエラーが発生しました: ${error.message}` 
      })
    };
  }
}; 