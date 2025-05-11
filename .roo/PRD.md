Great. I’ll create a Product Requirements Document (PRD) tailored to your AI coding assistant using the SPARC methodology for the 'Congressional Trading Analyzer'—a tool that answers user queries about congressional stock trades by generating insightful reports with graphs and commentary. It will include input types (e.g., stock tickers, politician names, time filters), user interface layout (chat + report panel), and a system designed for dynamic, multi-angle analysis.

I'll get started and let you know when it's ready for review.

# Congressional Trading Analyzer – Product Requirements Document (PRD)

## Specification

The _Congressional Trading Analyzer_ is a Streamlit-based AI application that lets users ask natural-language analytical questions about congressional stock trading. Users can query **specific stock tickers**, **individual members of Congress**, or combinations (e.g. “performance of Tesla stock vs. trades by Senator X”), with optional time filters (all time or custom date ranges). The system will ingest publicly available transaction records for the US Congress (using the HouseStockWatcher API and SenateStockWatcher API) and historical stock prices from Yahoo Finance (via the Python **yfinance** library). It will then compute metrics and generate visuals such as timelines, bar charts, and summary tables. For example, a query might return a chart of a stock’s price over time with congressional trade dates annotated, a comparison of trading frequency by member or ticker, and correlations between trades and committee assignments. Analysis goals include identifying trends like “most traded tickers”, “highest-return trades”, and whether committee memberships align with traded industries (a known line of inquiry).

- **User Queries:** Accept free-text questions about a ticker symbol, a congressperson’s name, or both, plus optional date range filters. Examples: “What trades did Rep. Smith make in energy stocks in 2023?” or “Show me Apple stock performance around Senator Doe’s trades.”
- **Data Ingestion:** Automatically fetch the latest disclosure data via the public **HouseStockWatcher** and **SenateStockWatcher** APIs. Complement this with historical stock price data from Yahoo Finance (using the open-source _yfinance_ Python package). (These sources provide publicly reported trade data and stock market prices for research.)
- **Analysis & Visualization:** Compute and display insights such as:

  - **Trade Timing vs. Performance:** Overlay trade dates on stock price charts, measure returns after buys/sells, and highlight whether trades precede market moves.
  - **Activity by Person/Ticker:** Summarize trade counts or volumes per Congress member or ticker (e.g. bar charts of top traders or most-active stocks).
  - **Committee Role Correlation:** Cross-reference each member’s committee assignments with the sectors of the stocks they trade (as in prior research), to flag potential conflicts or patterns.
  - **Aggregate Metrics:** Rank the “most traded” securities, highest-return trades, biggest portfolios, etc., and display key stats in tables or dashboards.

- **Prompt Refinement:** Use AI prompt engineering to preprocess user inputs. For example, apply a “Rephrase and Respond” technique: the system will automatically reword ambiguous or complex queries into clearer form before analysis. This helps ensure the user’s intent is captured and maximizes the relevance of downstream results.
- **User Interface:** Present a **dual-pane Streamlit UI**. The left sidebar (via `st.sidebar`) will host a chat-like input panel for queries. The main panel will show the results: interactive charts and graphs (using Plotly, e.g. with `st.plotly_chart`) and text summaries. Users can scroll or interact with charts (zoom, filter, hover for details) while the chat history persists in the sidebar.
- **Best Practices:** Ensure robust, maintainable engineering. No credentials are hard-coded; all API keys or secrets (if any) must be stored in environment variables or config files (e.g. using a `.env` file or Streamlit’s secrets management). Structure the code into modular Python components (separate modules for data fetching, processing, and UI). Maintain a high level of automated test coverage (especially for data handlers and analysis logic) – writing unit tests (e.g. with pytest) to validate correctness. Auto-generate documentation (using tools like Sphinx or MkDocs from docstrings) so that each module and function is documented. Follow coding best practices: clear naming, consistent style, error handling, and comprehensive testing.

&#x20;_The interface will display interactive charts for queries. For example, the main panel might overlay congressional trade dates on a historical stock price chart._ In this timeline view, users can visually correlate trade events (markers) with price movements. Other charts could include bar graphs of trade counts or return distributions. All plots will be rendered with Plotly (via Streamlit), allowing zooming, hovering tooltips, and filtering.

&#x20;_The app will also present aggregated summary data (e.g. trade volumes or returns by ticker) in tables or dashboards._ For instance, a table of “Top 10 Traded Stocks” or a heatmap of committee-sector correlations could be shown. These summaries give a quick overview of trading behavior (who trades what, and how profitable). Combined with the chat-panel explanation, users get both visual and textual analysis of congressional trading patterns.

## Pseudocode

- **On user query:** Parse the natural language input to identify focus (ticker symbol, legislator name, or both) and optional date range.
- **Query refinement:** Pass the input through a rephrasing function. (E.g., use an AI prompt: “Rephrase and clarify this question: _{user_query}_” to produce a cleaner intent statement.)
- **Data retrieval:**

  1. If query involves members of Congress, call the HouseStockWatcher and/or SenateStockWatcher APIs to fetch all reported trades for those individuals (filter by date range if specified).
  2. If query involves tickers, similarly fetch all trades involving those tickers (or fetch all trades then filter by ticker).
  3. For each relevant trade, use yfinance to download historical price data for the associated stock (covering from before trade date to present or to sale date).

- **Data processing:**

  1. For **trade timing vs. performance**, for each trade compute metrics like buy/sell date, price, subsequent price changes, and returns.
  2. For **activity summaries**, count trades by person and by ticker (e.g. a dictionary mapping person→{ticker: count}).
  3. For **committee correlations**, join each member’s committees (from a committee-membership dataset) with the GICS sector of each traded stock. Identify matches (e.g. member on Agriculture Committee trading Agri stocks).
  4. Compute any aggregate metrics requested (e.g. top N traded tickers, average return per member).

- **Visualization & output:**

  1. Generate Plotly figures: e.g., a line chart of stock price with vertical lines at trade dates; bar charts of trade counts; scatter plots of return vs. holding time.
  2. Create textual analysis: bullet points or paragraphs summarizing key findings (e.g. “Senator X traded Tesla twice in 2023, with a 15% gain each time…”).

- **Return results:** Output the charts and text into Streamlit UI. Keep chat history of question-answer in the sidebar for context.
- **Error Handling:** If a query yields no data (e.g. no trades found), return a friendly message. If APIs fail, retry or notify.

## Architecture

The system is organized into clearly separated modules and data flows:

- **User Interface (Streamlit Chat Panel):** A Streamlit frontend with two panes. The **sidebar** hosts the chat input and history using `st.sidebar`. The **main panel** displays results (embedded charts via `st.plotly_chart` and text outputs). The UI layer sends the user’s query text to the backend processing module and then renders the returned charts and analysis.
- **Query Processor:** An AI-assisted component (could use an LLM or prompt-driven logic) that reformulates and interprets user queries. This ensures the query is mapped to the right data retrieval and analysis steps (for example, detecting whether a question is about a ticker’s performance or a member’s portfolio). Prompt engineering techniques (such as the Rephrase-and-Respond strategy) improve the clarity of the query before analysis.
- **Data Ingestion:** Separate Python modules handle external data access. These include:

  - _CongressTradeFetcher:_ Calls the HouseStockWatcher and SenateStockWatcher REST APIs to get recent trade disclosures. It may cache responses or store raw CSV/JSON for reuse.
  - _StockPriceFetcher:_ Uses yfinance to fetch historical stock prices for queried tickers around specified dates.
  - _CommitteeDataLoader:_ Loads a static dataset of current congressional committee assignments (e.g. from the UnitedStates.io JSON) to link members to committees.

- **Data Processing & Analysis:** After ingestion, the _Analysis Engine_ correlates trades with prices and committees. It computes metrics (returns, trade frequencies) and prepares summary tables. All core logic lives here. This logic should be modular (e.g. functions for computing returns, generating summary stats, correlation analysis).
- **Visualization Module:** Generates interactive charts using Plotly. For instance, a `create_price_chart(trades, prices)` function might output a Plotly figure with annotations for each trade event. These figures are returned to the UI. The module follows Streamlit’s chart API to ensure integration.
- **Data Flow:** The flow is: **User query → Query Processor → (calls) Data Ingestion modules → Data Processing → Visualization/Text Generation → UI display**. Each module exposes well-defined interfaces (e.g. `fetch_trades(person, dates)` returns standardized data). Data passes between modules as pandas DataFrames or dictionaries.

&#x20;_Data and metrics flow through distinct components (illustrative stock ticker display)._ For example, a “CongressTradeFetcher” module retrieves raw trade numbers (as in the image’s stock board), which then pass to analysis routines. The architecture allows swapping or updating components (e.g. adding caching or a database) without altering others. APIs for external data are abstracted behind handler classes. This modular design supports testing each part in isolation.

## Refinement

To ensure code quality and maintainability, the codebase will be iteratively refined with these practices:

- **Modular Design:** Split functionality into clear files and classes (e.g. _fetchers.py_, _analysis.py_, _visuals.py_, _ui.py_). Each module has a single responsibility (data fetching, analysis, or UI). For example, a `TradeAnalyzer` class may depend on `CongressTradeFetcher` and `CommitteeDataLoader` but has no UI code.
- **Configuration and Secrets:** Use a `.env` file or Streamlit’s secrets for all API keys, and load them with `os.environ` or a config module (never hardcode credentials). Document required environment variables in README.
- **Testing:** Write comprehensive unit tests (using pytest). Tests cover data handlers (mock API responses, verify parsing), analysis functions (validate computed returns and correlations), and any utility logic. Aim for high coverage (e.g. 80%+) for critical modules, following best practices of thorough testing. Include tests for edge cases (no trades found, network failures).
- **Documentation:** Include docstrings for every function and class. Use a tool like Sphinx to auto-generate documentation websites from these docstrings. Also maintain high-level README or a docs folder explaining the overall architecture and how to run the app. Good documentation is part of “high-quality code” alongside testing and modularity.
- **Iterative Improvement:** After an initial prototype, review code for refactoring opportunities. Use linters (flake8/flake8) and formatters (Black) to enforce style. For example, factor out duplicate code (e.g. repeated API call patterns) into common utilities. Refine prompt-engineering templates based on early user feedback (the LLM prompt in the query processor may evolve). Run performance profiling if needed for large data sets. This step also involves writing integration tests and possibly adding continuous integration (CI) scripts to run tests on commits.

## Completion

The project is considered successful when the following criteria are met:

- **Correctness:** For a variety of test queries, the app returns sensible analyses. For example, sample queries about known trade events produce accurate charts (visual verification) and logical narrative answers. Unit tests in the _data fetching_ and _analysis_ modules all pass, ensuring correctness of core computations.
- **UI/UX:** The Streamlit interface cleanly separates input and output. The sidebar chat input is responsive, and charts in the main panel render without errors. Manual testing (or automated UI tests) confirm that charts update appropriately for different queries.
- **Robustness:** The app handles edge cases (e.g. no data available) gracefully with user-friendly messages. Mock failures of the House/Senate API should not crash the app (errors are caught and reported).
- **Test Coverage:** Automated tests cover all major paths. For example, data handlers and analysis functions each have dedicated tests, with coverage above an agreed threshold (e.g. ≥80%). CI/CD pipelines (if set up) succeed.
- **Documentation:** All modules have up-to-date docstrings. An auto-generated documentation site (via Sphinx or similar) exists covering how each component works. The README describes setup (including environment variables) and usage examples.

Upon completion of these criteria, the system will be ready for deployment. The PRD’s SPARC structure ensures each aspect of the project—features, design logic, and quality standards—is clearly defined and documented for the AI assistant team to implement.

**Sources:** Public stock transaction data from HouseStockWatcher and SenateStockWatcher and stock prices via Yahoo Finance; streamlit layout with sidebar and charts; prompt refinement technique; coding best-practices (no hardcoding secrets, modular design, testing).
