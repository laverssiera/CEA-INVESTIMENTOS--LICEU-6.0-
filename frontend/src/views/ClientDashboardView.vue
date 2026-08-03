<template>
  <div class="page">
    <section class="hero">
      <div>
        <p class="eyebrow">Cliente</p>
        <h2>Painel do cliente para acompanhar financiamento, documentos e comunicação.</h2>
        <p>
          O dashboard do cliente centraliza evolução do crédito, entregas documentais e visão de
          relacionamento com a operação financeira.
        </p>
      </div>

      <div class="hero-grid">
        <div class="card">
          <small>Status do pedido</small>
          <div class="stat-value">Em análise</div>
          <span class="tag info">Documentação ativa</span>
        </div>
        <div class="card">
          <small>Próxima etapa</small>
          <div class="stat-value">Comitê</div>
          <span class="tag warning">Risco + crédito</span>
        </div>
      </div>
    </section>

    <section class="grid-2">
      <article class="panel">
        <small>Resumo</small>
        <h3>Timeline do financiamento</h3>
        <ul class="list">
          <li>cadastro recebido;</li>
          <li>documentos em validação;</li>
          <li>análise de crédito em andamento;</li>
          <li>aguardando deliberação final.</li>
        </ul>
      </article>

      <article class="panel">
        <small>Comunicação</small>
        <h3>Itens recentes</h3>
        <ul class="list">
          <li>solicitação de comprovação de titularidade do terreno;</li>
          <li>relatório preliminar de risco disponível;</li>
          <li>janela prevista para retorno: até 3 dias úteis.</li>
        </ul>
      </article>
    </section>
  </div>
</template>