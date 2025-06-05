import { useEffect, useState } from 'react';
import { styles } from '../styles/commonStyles';

export default function RecipeScreen({ setScreen, setSelectedRecipe }) {
  const [recipeList, setRecipeList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const res = await fetch('http://localhost:8000/recommend');
        const data = await res.json();
        const all = [...(data.exact || []), ...(data.near || [])];
        setRecipeList(all);
      } catch (err) {
        console.error('레시피 불러오기 실패:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, []);

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <button style={styles.backBtn} onClick={() => setScreen('home')}>←</button>
        <span>추천 레시피</span>
        <span></span>
      </div>

      {loading ? (
        <p>로딩 중...</p>
      ) : recipeList.length === 0 ? (
        <p>추천 가능한 레시피가 없습니다.</p>
      ) : (
        recipeList.map((recipe, idx) => (
          <div
            key={idx}
            style={{ ...styles.recipeCard, cursor: 'pointer' }}
            onClick={() => {
              setSelectedRecipe(recipe);
              setScreen('recipeDetail');
            }}
          >
            <div style={{ fontWeight: 'bold' }}>{recipe.title}</div>
            {recipe.missing?.length > 0 && (
              <div style={{ fontSize: '0.9em', color: '#888' }}>
                부족한 재료: {recipe.missing.join(', ')}
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
}
