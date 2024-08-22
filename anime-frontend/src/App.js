import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
    const [city, setCity] = useState('');
    const [data, setData] = useState(null);

    const fetchWeather = () => {
        axios.get(`http://127.0.0.1:8000/api/weather/${city}/`)
            .then(response => setData(response.data))
            .catch(error => console.error('Error fetching data:', error));
    }

    return (
        <div className="min-h-screen animated-wavy-gradient flex flex-col items-center justify-center py-6">
            <div className="bg-white shadow-md rounded-lg p-8 max-w-lg w-full">
                <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
                    Weather-Based Anime Recommendation
                </h1>
                <div className="mb-4">
                    <input 
                        type="text" 
                        value={city} 
                        onChange={(e) => setCity(e.target.value)} 
                        placeholder="Enter city"
                        className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                    />
                </div>
                <button 
                    onClick={fetchWeather}
                    className="w-full bg-blue-500 text-white p-3 rounded-lg hover:bg-blue-600"
                >
                    Get Recommendation
                </button>
                {data && (
                    <div className="mt-6">
                        <h2 className="text-xl font-semibold text-gray-700">
                            City: {data.city}
                        </h2>
                        <h3 className="text-xl font-semibold text-gray-700 mt-2">
                            Weather: {data.description}
                        </h3>
                        <p className="text-gray-600">Temperature: {data.temperature}</p>
                        <p className="text-gray-600">Wind: {data.wind}</p>
                        <h3 className="text-lg font-medium text-gray-700 mt-4">Recommended Anime Genre:</h3>
                        <p className="text-gray-700">{data.recommended_genre}</p>  {/* Display the genre */}
                        <h3 className="text-lg font-medium text-gray-700 mt-4">Recommended Anime:</h3>
                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                            {data.recommended_anime.map(anime => (
                                <div key={anime.mal_id} className="relative bg-white rounded-lg shadow-md overflow-hidden">
                                    <img 
                                        src={anime.thumbnail_url} 
                                        alt={anime.title} 
                                        className="w-full h-32 sm:h-48 object-cover"
                                    />
                                    <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4">
                                        <h4 className="text-lg font-semibold text-white">{anime.title}</h4>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
