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
  const [userId, setUserId] = useState(null);     // 로그인된 사용자 ID
  const [nickname, setNickname] = useState(null); // 사용자 닉네임

  if (screen === 'login')
    return (
      <LoginScreen
        setScreen={setScreen}
        setUserId={setUserId}
        setNickname={setNickname}
      />
    );

  if (screen === 'signup')
    return <SignupScreen setScreen={setScreen} />;

  if (screen === 'home')
    return <HomeScreen setScreen={setScreen} nickname={nickname} />;

  if (screen === 'input')
    return (
      <InputScreen
        ingredients={ingredients}
        setIngredients={setIngredients}
        input={input}
        setInput={setInput}
        setScreen={setScreen}
        userId={userId}
      />
    );

  if (screen === 'recipe')
    return (
      <RecipeScreen
        setScreen={setScreen}
        setSelectedRecipe={setSelectedRecipe}
        ingredients={ingredients}
        userId={userId}
      />
    );

  if (screen === 'recipeDetail' && selectedRecipe)
    return (
      <RecipeDetailScreen
        recipe={selectedRecipe}
        setScreen={setScreen}
        userId={userId}
      />
    );

  if (screen === 'camera')
    return (
      <CameraScreen
        setScreen={setScreen}
        setIngredients={setIngredients}
        userId={userId}
      />
    );

  return null;
}

export default App;
