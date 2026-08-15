import { useEffect, useRef, useState } from "react";
import {
  ArrowRight,
  Check,
  Plus,
  X,
} from "@phosphor-icons/react";

const YANDEX_FORM_SRC = "https://forms.yandex.ru/cloud/6a7c4aee84227c21082bae01?iframe=1";
const YANDEX_EMBED_SCRIPT = "https://forms.yandex.ru/_static/embed.js";

const heroProducts = [
  {
    number: "1",
    name: "Светильник Orbit",
    category: "Подвесной светильник",
    price: 18900,
    dimensions: "Ø 600 × 120 мм",
    material: "Матовый металл · чёрный",
    image: "/assets/product-lamp.png",
  },
  {
    number: "2",
    name: "Стол Column",
    category: "Обеденный стол",
    price: 89500,
    dimensions: "Ø 1100 × 750 мм",
    material: "Травертин · натуральный",
    image: "/assets/product-table.png",
  },
];

const budgetModes = {
  rational: {
    label: "Рациональный",
    range: "~1,5–3,4 млн ₽",
    image: "/assets/budget-rational-v3.png",
    summary: "Серийная мебель, простые материалы, базовый свет",
  },
  comfort: {
    label: "Комфорт",
    range: "~3,5–5,9 млн ₽",
    image: "/assets/budget-comfort-v3.png",
    summary: "Качественные материалы, бренды среднего сегмента",
  },
  premium: {
    label: "Премиальный",
    range: "~6–10+ млн ₽",
    image: "/assets/budget-premium-v3.png",
    summary: "Натуральный камень, заказные изделия, коллекционный свет",
  },
};

const budgetSlider = { min: 1500000, max: 10000000, rationalLimit: 3400000, comfortLimit: 5900000 };

const sofaVariants = {
  current: { label: "Картос", price: 90990, delta: 0, image: "/assets/sofa-room-v3-current.png" },
  cheaper: { label: "Сваут", price: 71990, delta: -19000, image: "/assets/sofa-room-v3-cheaper.png" },
  compact: { label: "Маиль", price: 60990, delta: -30000, image: "/assets/sofa-room-v3-compact.png" },
  color: { label: "Картос · олива", price: 90990, delta: 0, image: "/assets/sofa-room-v3-color.png" },
};

const exampleProjects = [
  { title: "Студия · 28 м²", description: "Для первой квартиры, аренды или компактного ремонта.", image: "/assets/example-studio.png" },
  { title: "Однокомнатная · 42 м²", description: "Для базового обновления и полной комплектации.", image: "/assets/example-onebed.png" },
  { title: "Двухкомнатная · 64 м²", description: "Для семейного сценария и более сложного подбора.", image: "/assets/example-twobed.png" },
];

const faqItems = [
  {
    question: "Нужен ли именно план квартиры?",
    answer: "Нет. План с размерами лучше сохраняет геометрию, но для первого результата можно загрузить фотографию комнаты.",
  },
  {
    question: "Можно ли загрузить только фото?",
    answer: "Да. Сервис соберёт концепцию по видимой части интерьера, а неизвестные размеры и скрытые зоны отметит как допущения.",
  },
  {
    question: "Это реальные товары или похожие варианты?",
    answer: "В финальном сервисе — реальные товары с артикулами, ценами и ссылками. Пока каталоги подключаются, часть позиций в раннем доступе может быть ориентиром и будет явно отмечена.",
  },
  {
    question: "Насколько точен бюджет?",
    answer: "Это ориентир для принятия решения. Точность зависит от города, площади, состояния квартиры и выбранных товаров; итог уточняется после проверки исходных данных.",
  },
  {
    question: "Подходит ли сервис для одной комнаты?",
    answer: "Да. Можно начать с одной комнаты, подобрать направление, ключевые предметы и бюджет именно для неё.",
  },
  {
    question: "Подходит ли сервис для всей квартиры?",
    answer: "Да. Квартира собирается последовательно по комнатам, но в единой палитре, логике материалов и уровне бюджета.",
  },
  {
    question: "Это заменяет дизайн-проект?",
    answer: "Нет. РАМКА помогает выбрать выполнимую концепцию до рабочего проекта. Чертежи, инженерные решения и авторский надзор остаются задачей дизайнера и профильных специалистов.",
  },
];

const formatPrice = (value) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const formatMillions = (value) => {
  const millions = value / 1000000;
  return `${millions.toLocaleString("ru-RU", { minimumFractionDigits: Number.isInteger(millions) ? 0 : 1, maximumFractionDigits: 1 })} млн ₽`;
};

function track(name, payload = {}) {
  const detail = { event: name, ...payload };
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push(detail);
  window.dispatchEvent(new CustomEvent("landing:event", { detail }));
}

function Brand({ variant = "wordmark" }) {
  const isMark = variant === "mark";

  return (
    <a className={`brand${isMark ? " brand--mark" : ""}`} href="#top" aria-label="РАМКА — на главную">
      <img src={isMark ? "/assets/ramka-icon.svg" : "/assets/ramka-ai-logo.svg"} alt="" />
    </a>
  );
}

function ProductDrawer({ selected, onSelect, onClose }) {
  if (selected === null) return null;
  const product = heroProducts[selected];

  return (
    <div className="product-drawer" role="dialog" aria-modal="true" aria-labelledby="product-title" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <aside className="product-drawer__panel">
        <header className="product-drawer__header">
          <span>Предмет {product.number} из {heroProducts.length}</span>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Закрыть карточку товара">
            <X size={21} weight="light" />
          </button>
        </header>
        <div className={`product-drawer__image ${selected === 0 ? "product-drawer__image--lamp" : ""}`}>
          <img src={product.image} alt={product.name} />
        </div>
        <div className="product-drawer__body">
          <p>{product.category}</p>
          <h2 id="product-title">{product.name}</h2>
          <strong>{formatPrice(product.price)}</strong>
          <dl>
            <div><dt>Размеры</dt><dd>{product.dimensions}</dd></div>
            <div><dt>Материал</dt><dd>{product.material}</dd></div>
          </dl>
        </div>
        <nav className="product-drawer__switcher" aria-label="Другие товары в интерьере">
          {heroProducts.map((item, index) => (
            <button className={selected === index ? "is-active" : ""} type="button" key={item.number} onClick={() => onSelect(index)}>
              <span>{item.number}</span>
              <img src={item.image} alt="" />
              <b>{item.name}</b>
            </button>
          ))}
        </nav>
      </aside>
    </div>
  );
}

function BudgetVisual({ active }) {
  const [outgoingImage, setOutgoingImage] = useState(null);
  const currentImage = useRef(active.image);

  useEffect(() => {
    if (currentImage.current === active.image) return undefined;
    setOutgoingImage(currentImage.current);
    currentImage.current = active.image;
    const timer = window.setTimeout(() => setOutgoingImage(null), 540);
    return () => window.clearTimeout(timer);
  }, [active.image]);

  return (
    <div className="budget-configurator__visual">
      <img src={active.image} alt={`Интерьер в сценарии «${active.label}»`} />
      {outgoingImage && <img className="budget-image--outgoing" src={outgoingImage} alt="" aria-hidden="true" />}
    </div>
  );
}

function WaitlistModal({ open, onClose }) {
  useEffect(() => {
    if (!open) return;
    const onKey = (event) => event.key === "Escape" && onClose();
    document.body.classList.add("modal-open");
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.classList.remove("modal-open");
      window.removeEventListener("keydown", onKey);
    };
  }, [open, onClose]);

  useEffect(() => {
    if (!open) return undefined;

    const existingScript = document.querySelector(`script[src="${YANDEX_EMBED_SCRIPT}"]`);
    const notifyEmbed = () => window.dispatchEvent(new Event("resize"));

    if (existingScript) {
      notifyEmbed();
      return undefined;
    }

    const script = document.createElement("script");
    script.src = YANDEX_EMBED_SCRIPT;
    script.async = true;
    script.dataset.yandexFormsEmbed = "true";
    script.addEventListener("load", notifyEmbed, { once: true });
    document.head.appendChild(script);

    return () => script.removeEventListener("load", notifyEmbed);
  }, [open]);

  if (!open) return null;

  return (
    <div className="modal modal--form" role="dialog" aria-modal="true" aria-labelledby="waitlist-title" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <div className="modal__sheet modal__sheet--form">
        <button className="modal__close icon-button" type="button" onClick={onClose} aria-label="Закрыть форму">
          <X size={21} weight="light" />
        </button>
        <div className="yandex-form-modal__intro">
          <span>Ранний доступ</span>
          <h2 id="waitlist-title">Первая концепция<br />для вашей квартиры.</h2>
        </div>
        <div className="yandex-form-modal__frame-wrap">
          <iframe
            className="yandex-form-modal__frame"
            src={YANDEX_FORM_SRC}
            name="ya-form-6a7c4aee84227c21082bae01"
            title="Форма раннего доступа к РАМКЕ"
            frameBorder="0"
            loading="eager"
            onLoad={() => track("yandex_form_loaded")}
          />
        </div>
      </div>
    </div>
  );
}

export function App() {
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [budgetValue, setBudgetValue] = useState(4200000);
  const [sofaVariant, setSofaVariant] = useState("current");
  const [modalOpen, setModalOpen] = useState(false);
  const activeBudget = budgetValue <= budgetSlider.rationalLimit ? "rational" : budgetValue <= budgetSlider.comfortLimit ? "comfort" : "premium";
  const active = budgetModes[activeBudget];
  const sofa = sofaVariants[sofaVariant];
  const budgetProgress = ((budgetValue - budgetSlider.min) / (budgetSlider.max - budgetSlider.min)) * 100;

  useEffect(() => track("hero_view"), []);

  const openProduct = (index) => {
    setSelectedProduct(index);
    track("product_viewed", { product: heroProducts[index].name });
  };

  const changeBudget = (value) => {
    const nextValue = Number(value);
    const nextBudget = nextValue <= budgetSlider.rationalLimit ? "rational" : nextValue <= budgetSlider.comfortLimit ? "comfort" : "premium";
    setBudgetValue(nextValue);
    track("budget_adjusted", { budget: nextBudget, total: nextValue });
  };

  const openWaitlist = () => {
    setModalOpen(true);
    track("primary_cta_clicked", { budget: activeBudget });
  };

  return (
    <main id="top">
      <header className="site-header">
        <Brand />
        <nav aria-label="Основная навигация">
          <a href="#process">Как работает</a>
          <a href="#budget">Бюджет</a>
          <a href="#deliverables">Что получите</a>
        </nav>
        <button className="header-cta" type="button" onClick={openWaitlist}>Ранний доступ <ArrowRight size={16} /></button>
      </header>

      <section className="hero" aria-labelledby="hero-title">
        <img className="hero__image" src="/assets/interior-comfort.png" alt="Интерьер кухни-гостиной по плану квартиры" />
        <div className="hero__veil" />
        <div className="hero__copy">
          <h1 id="hero-title">Интерьер,<br />который можно<br />воплотить.</h1>
          <p>Загрузите план или фото квартиры — получите интерьер, реальные товары и ориентир бюджета.</p>
          <div className="hero__actions">
            <button className="button button--primary" type="button" onClick={openWaitlist}>Получить ранний доступ <ArrowRight size={18} /></button>
          </div>
        </div>
        <button className="product-pin product-pin--one" type="button" onClick={() => openProduct(0)} aria-label="Открыть карточку светильника">1</button>
        <button className="product-pin product-pin--two" type="button" onClick={() => openProduct(1)} aria-label="Открыть карточку стола">2</button>
      </section>

      <section className="process-section" id="process" aria-labelledby="process-title">
        <div className="section-heading section-heading--wide">
          <h2 id="process-title">От плана — к собранному интерьеру.</h2>
        </div>
        <div className="process-board">
          <article className="process-board__plan">
            <header className="process-board__head">
              <span>01</span>
              <h3>План или фото квартиры</h3>
            </header>
            <img src="/assets/floor-plan.png" alt="Исходный план квартиры" />
          </article>
          <div className="process-board__arrow process-board__arrow--first" aria-hidden="true"><ArrowRight size={24} weight="light" /></div>
          <article className="process-board__interior">
            <header className="process-board__head">
              <span>02</span>
              <h3>Интерьерная концепция</h3>
            </header>
            <img src="/assets/process-interior.png" alt="Интерьерная концепция по плану" />
          </article>
          <div className="process-board__arrow process-board__arrow--second" aria-hidden="true"><ArrowRight size={24} weight="light" /></div>
          <aside className="project-cart">
            <div className="project-cart__head"><span>03</span><h3>Товары и смета</h3></div>
            <div className="project-cart__item"><i className="project-cart__thumb project-cart__thumb--chair" /><span>Кресло для чтения</span><strong>от 62 000 ₽</strong></div>
            <div className="project-cart__item"><i className="project-cart__thumb project-cart__thumb--table" /><span>Журнальный стол</span><strong>от 48 000 ₽</strong></div>
            <div className="project-cart__item project-cart__item--summary"><span>Ещё 18 позиций</span><strong>от 1 140 000 ₽</strong></div>
            <div className="project-cart__total"><span>Реальные товары · артикулы и ссылки</span><strong>от 1 250 000 ₽</strong></div>
          </aside>
        </div>
      </section>

      <section className="budget-section" id="budget" aria-labelledby="budget-title">
        <div className="section-heading">
          <h2 id="budget-title">Бюджет меняет интерьер.</h2>
        </div>
        <div className="budget-configurator">
          <aside className="budget-ledger" aria-live="polite">
            <div className="budget-slider">
              <div className="budget-slider__value">
                <span>Бюджет реализации</span>
                <strong>{formatMillions(budgetValue)}</strong>
              </div>
              <input
                aria-label="Бюджет реализации для квартиры"
                type="range"
                min={budgetSlider.min}
                max={budgetSlider.max}
                step="100000"
                value={budgetValue}
                onChange={(event) => changeBudget(event.target.value)}
                style={{ "--slider-progress": `${budgetProgress}%` }}
              />
              <div className="budget-slider__scale" aria-hidden="true"><span>1,5 млн</span><span>10+ млн</span></div>
            </div>
            <div className="budget-ledger__estimate">
              <span>{active.label}</span>
              <strong>{active.range}</strong>
              <p>{active.summary}</p>
            </div>
            <div className="budget-ledger__meta">
              <span>Пример для квартиры 52 м²</span>
            </div>
          </aside>
          <BudgetVisual active={active} />
        </div>
      </section>

      <section className="swap-section" id="result" aria-labelledby="swap-title">
        <div className="swap-section__visual">
          <img key={sofa.image} src={sofa.image} alt={`Интерьер с диваном: ${sofa.label}`} />
        </div>
        <div className="swap-section__panel">
          <h2 id="swap-title">Не подходит диван?<br />Поменяем только его.</h2>
          <p>Комната остаётся прежней. В финальном сервисе меняется существующий товар из подключённого каталога — вместе с артикулом, ценой и ссылкой.</p>
          <div className="swap-options" role="radiogroup" aria-label="Вариант дивана">
            {Object.entries(sofaVariants).map(([key, item]) => (
              <button key={key} className={sofaVariant === key ? "is-active" : ""} type="button" role="radio" aria-checked={sofaVariant === key} onClick={() => {
                setSofaVariant(key);
                track("product_replaced", { replacement: key });
              }}>
                <span>{item.label}</span><strong>{formatPrice(item.price)}</strong>
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="deliverables" id="deliverables" aria-labelledby="deliverables-title">
        <div className="section-heading"><h2 id="deliverables-title">Что вы получаете<br />после генерации.</h2></div>
        <div className="result-grid" aria-label="Состав результата">
          <article className="result-card">
            <div className="result-card__preview result-card__preview--render">
              <img src="/assets/result-concept-v2.png" alt="Новая интерьерная концепция гостиной" />
            </div>
            <h3>Интерьерная концепция</h3>
            <p>2–4 визуализации комнаты в выбранном стиле.</p>
          </article>
          <article className="result-card">
            <div className="result-card__preview result-card__preview--products">
              <img src="/assets/result-products-v2.png" alt="Диван, стол и светильник из соседней интерьерной концепции" />
            </div>
            <h3>Подбор реальных товаров</h3>
            <p>Артикулы, ссылки, цены и замены по ключевым позициям.</p>
          </article>
          <article className="result-card">
            <div className="result-card__preview result-card__preview--budget">
              <span>Ориентир по квартире</span>
              <strong>~4,2 млн ₽</strong>
              <dl>
                <div><dt>Отделка</dt><dd>1,4 млн</dd></div>
                <div><dt>Мебель и свет</dt><dd>2,1 млн</dd></div>
                <div><dt>Работы</dt><dd>0,7 млн</dd></div>
              </dl>
            </div>
            <h3>Ориентир бюджета</h3>
            <p>Смета по комнате или квартире с разбивкой по категориям.</p>
          </article>
          <article className="result-card">
            <div className="result-card__preview result-card__preview--document">
              <img src="/assets/result-pdf-pages-v6-ramka-transparent.png" alt="Повернутые страницы PDF-документа РАМКА без фона" />
            </div>
            <h3>PDF-документ</h3>
            <p>Краткое описание концепции, список товаров и итоговая стоимость.</p>
          </article>
        </div>
      </section>

      <section className="examples" aria-labelledby="examples-title">
        <div className="section-heading section-heading--split">
          <h2 id="examples-title">Квартиры<br />разного масштаба.</h2>
        </div>
        <div className="examples__grid">
          {exampleProjects.map((project) => (
            <article className="project-card" key={project.title}>
              <img src={project.image} alt={`${project.title}, интерьерная концепция`} />
              <div><h3>{project.title}</h3><p>{project.description}</p></div>
            </article>
          ))}
        </div>
      </section>

      <section className="offer-section" id="access" aria-labelledby="offer-title">
        <div className="offer-section__title">
          <h2 id="offer-title">Первая концепция<br />для вашей квартиры.</h2>
          <p>Оставьте заявку сейчас, чтобы попасть в первую группу и помочь нам настроить сервис на реальных планах и бюджетах.</p>
        </div>
        <article className="offer-card">
          <header><span>Ранний доступ</span><strong>Бесплатно</strong></header>
          <ul>
            <li><Check size={18} /> Приоритет в первой группе</li>
            <li><Check size={18} /> Концепция по плану или фото</li>
            <li><Check size={18} /> Реальные товары и альтернативы</li>
          </ul>
          <button className="button button--primary" type="button" onClick={openWaitlist}>Получить ранний доступ <ArrowRight size={18} /></button>
        </article>
      </section>

      <section className="faq" id="faq" aria-labelledby="faq-title">
        <div className="section-heading"><h2 id="faq-title">Частые вопросы.</h2></div>
        <div className="faq__list">
          {faqItems.map((item) => (
            <details key={item.question}>
              <summary>{item.question}<Plus size={21} weight="light" aria-hidden="true" /></summary>
              <p>{item.answer}</p>
            </details>
          ))}
        </div>
      </section>

      <footer className="site-footer">
        <Brand variant="mark" />
        <nav className="site-footer__legal" aria-label="Юридическая информация">
          <span>Политика обработки данных</span>
          <span>Согласие на обработку данных</span>
          <span>Пользовательское соглашение</span>
        </nav>
        <span>© 2026 · Ранний доступ</span>
      </footer>

      <ProductDrawer selected={selectedProduct} onSelect={setSelectedProduct} onClose={() => setSelectedProduct(null)} />
      <WaitlistModal open={modalOpen} onClose={() => setModalOpen(false)} />
    </main>
  );
}
