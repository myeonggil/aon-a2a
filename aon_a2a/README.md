# Solve problem

- multiagent-orchestration: create and manage multiple agents that can collaborate in realtime
- Tool Integration: Easily connect agents with external tools and APIs
- Flexible Workflows: Support both autonomous and human-in-the-loop conversation patterns
- Code Generation & Execution: Enable agents to write, review, and execute code safely

- https://microsoft.github.io/autogen/0.2/docs/topics/non-openai-models/cloud-groq/

## AON Scenario
- 현재 배포된 AWS, Terraform 관련된 것은 테스트에 불과하다
- 주식과 관련된 주제, 개발 기술과 관련된 주제 등 재미있는 요소들을 생각해보자

## Stock?
1. 특정 분야에 대한 정보를 요구한다
- Example
  ```
  나는 현재 어떤 분야에 대해 궁금하여 현재 주가가 어떻게 변화했으며 관련된 기사를 찾아 상승과 하락한 시점에 대해 알고싶다
  ```
2. 예측이 주가 아닌 정확한 사실에 근거해야한다
3. 데이터의 계산이 정확해야한다(자본금에 의해 당시 시세에서 매수, 매도에 대한 계산)

## Trend?
1. 단순한 LLM에서 AI Agent의 발전으로 점점 완성되어가는 생각이든다
- Example
  ```
  AWS 클라우드와 Terraform을 대상으로 개발하였기 때문에 기술 블로그나 이슈 등을 분석하여 요약해주고 어떤식으로 사용하면 좋을지 best practice를 알려준다
  ```
2. AWS의 기술 블로그는 RSS 방식으로 feed에 접근하면 될 것 같다
3. Terraform이나 최신 트렌드 기술 제공 사이트나 API를 통해 접근
