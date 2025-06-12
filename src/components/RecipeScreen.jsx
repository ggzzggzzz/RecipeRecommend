import { useEffect, useState } from 'react';
import { styles } from '../styles/commonStyles';

export default function RecipeScreen({ setScreen, setSelectedRecipe, userId }) {
  const [recipeList, setRecipeList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!userId) return; // userId 없을 경우 API 호출 생략

    const fetchRecipes = async () => {
      try {
        const res = await fetch(`http://localhost:8000/recommend-from-db?user_id=${userId}`);
        const data = await res.json();
        setRecipeList(data.recommended || []);
      } catch (err) {
        console.error('레시피 불러오기 실패:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, [userId]);

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
            style={{
              backgroundColor: '#fff',
              padding: '12px',
              marginBottom: '12px',
              borderRadius: '12px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '12px'
            }}
            onClick={() => {
              console.log("레시피 객체 확인:", recipe);
              setSelectedRecipe(recipe);
              setScreen('recipeDetail');
            }}
          >
            <img
              src={recipe.image_url}
              alt="레시피 이미지"
              style={{
                width: '100px',
                height: '100px',
                objectFit: 'cover',
                borderRadius: '8px'
              }}
            />
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>{recipe.title}</div>
              <div style={{ fontSize: '0.9em', color: '#666', marginTop: '4px' }}>
                {recipe.description?.length > 60
                  ? recipe.description.slice(0, 60) + '...'
                  : recipe.description}
              </div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
