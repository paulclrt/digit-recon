import logo from './logo.svg';
import './App.css';

import {useState} from 'react'

import DrawingBox from './components/Drawing';
import Results from './components/Results'

function App() {

  const [arr, setArr] = useState([])
  
  function handlePredecitonFromDrawingBox (data) {
    console.log(...data.preds)
    setArr(data.preds)
  }


  return (
    <div className="App">
      <h1>Digit recognition</h1>
      <p>Draw a digit on the canva and hit send once done <br/>The results will be shown bellow. Please to improve the model click on the number you drew. <br/>thanks :)</p>
      <DrawingBox dataToParent={handlePredecitonFromDrawingBox}></DrawingBox>
      <Results results_array={arr}></Results>
    </div>
  );
}

export default App;
