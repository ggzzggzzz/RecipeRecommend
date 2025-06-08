import { useState } from 'react';
import HomeScreen from './components/HomeScreen';
import InputScreen from './components/InputScreen';
import RecipeScreen from './components/RecipeScreen';
import CameraScreen from './components/CameraScreen';
import RecipeDetailScreen from './components/RecipeDetailScreen';
import LoginScreen from './components/LoginScreen';
import SignupScreen from './components/SignupScreen';

function App() {
  const [screen, setScreen] = useState('home');
  const [ingredients, setIngredients] = useState([]);
  const [input, setInput] = useState('');
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  if (screen === 'home') return <HomeScreen setScreen={setScreen} />;
  if (screen === 'input')
    return (
      <InputScreen
        ingredients={ingredients}
        setIngredients={setIngredients}
        input={input}
        setInput={setInput}
        setScreen={setScreen}
      />
    );
  if (screen === 'recipe')
    return (
      <RecipeScreen
        setScreen={setScreen}
        setSelectedRecipe={setSelectedRecipe}
        ingredients={ingredients}
      />
    );
  if (screen === 'recipeDetail' && selectedRecipe)
    return (
      <RecipeDetailScreen
        recipe={selectedRecipe}
        setScreen={setScreen}
      />
    );
  if (screen === 'camera')
    return (
      <CameraScreen
        setScreen={setScreen}
        setIngredients={setIngredients}
      />
    );
  if (screen === 'login') return <LoginScreen setScreen={setScreen} />;
  if (screen === 'signup') return <SignupScreen setScreen={setScreen} />;
  return null;
}

export default App;
