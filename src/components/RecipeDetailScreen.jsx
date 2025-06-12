import { useEffect, useState } from 'react';
import { styles } from '../styles/commonStyles';

export default function RecipeDetailScreen({ setScreen, recipe }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!recipe) return;

    const fetchDetail = async () => {
      try {
        const res = await fetch(`http://localhost:8000/recipe-detail?recipe_id=${recipe.recipe_id}`);
        const data = await res.json();
        setDetail(data);
      } catch (err) {
        console.error("레시피 상세 조회 실패:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDetail();
  }, [recipe]);

  if (!recipe || loading) return <div style={styles.container}>로딩 중...</div>;

  if (!detail) return <div style={styles.container}>레시피 정보를 불러올 수 없습니다.</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <button style={styles.backBtn} onClick={() => setScreen('recipe')}>←</button>
        <span>레시피 상세</span>
        <span></span>
      </div>

      <img
        src={detail.image_url}
        alt="레시피 이미지"
        style={{ width: '100%', maxHeight: 250, objectFit: 'cover', borderRadius: '12px', marginBottom: 16 }}
      />

      <div style={{ padding: '0 16px' }}>
        <h2>{detail.name}</h2>
        <p style={{ color: '#555' }}>{detail.description}</p>

        <h3 style={{ marginTop: '24px' }}>사용된 식재료</h3>
        <ul>
          {detail.ingredients.map((ing, idx) => (
            <li key={idx} style={{ marginBottom: 8 }}>
              <strong>{ing.name}</strong> - {ing.qty_text || ing.qty} {ing.unit}
              {ing.price != null && (
                <> (예상 비용: {ing.price.toLocaleString()}원)</>
              )}
            </li>
          ))}
        </ul>

        <h3>총 재료비: {detail.total_price.toLocaleString()}원</h3>

        <a
          href={detail.recipe_url}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: 'inline-block',
            marginTop: '16px',
            padding: '10px 16px',
            backgroundColor: '#4CAF50',
            color: 'white',
            textDecoration: 'none',
            borderRadius: '8px'
          }}
        >
          전체 레시피 보기
        </a>
      </div>
    </div>
  );
}
