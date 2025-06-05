import React from 'react';
import { styles } from '../styles/commonStyles';

export default function RecipeDetailScreen({ recipe, setScreen }) {
  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <button style={styles.backBtn} onClick={() => setScreen('recipe')}>←</button>
        <span>레시피 상세</span>
        <span></span>
      </div>

      <div style={styles.recipeCard}>
        <h2>{recipe.title}</h2>
        <p>부족한 재료: {recipe.missing.length > 0 ? recipe.missing.join(', ') : '없음'}</p>
        <a href={recipe.url} target="_blank" rel="noopener noreferrer">
          👉 레시피 보러가기
        </a>
      </div>
    </div>
  );
}
