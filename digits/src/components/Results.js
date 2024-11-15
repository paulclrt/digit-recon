import react, {useRef} from 'react'
import "./Results.css"


function Results  ({results_array}) {

    var results = []
    results = [...results_array];

    const normalize = (value, min, max) => (value - min) / (max - min);

    const getColor = (normalizedValue) => {
        const r = Math.floor(255 * (1 - normalizedValue));    // Red component (decreases as value increases)
        const g = Math.floor(255 * normalizedValue);          // Green component (increases as value increases)
        const b = 0;  // Blue component stays 0 for a red-to-green gradient
        const a = 80;
        return `rgb(${r}, ${g}, ${b}, ${a})`;  // Return RGB value
    };

    const minValue = Math.min(...results); 
    const maxValue = Math.max(...results);
  

    return (
        <div className='results'>
            <ul>
                {results.map((prediction, index) => {
                    const normalized = normalize(prediction, minValue, maxValue);
                    const color = getColor(normalized);

                    return (
                        <li key={index} style={{ backgroundColor: color }}>
                            <div>
                                <p>
                                    {index}
                                <br/>
                                    {prediction.toFixed(5)*100}%
                                </p>
                            </div>
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}


export default Results;