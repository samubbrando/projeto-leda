library(ggplot2)
library(stringr)
library(dplyr)

input_dir <- "/home/nicolas/Downloads/SkipList-setup-a-search-sequential"
output_dir <- "/home/nicolas/Downloads/SkipList-setup-a-search-sequential/plots"
arquivos <- list.files(input_dir, pattern = "\\.txt$", full.names = TRUE, recursive = TRUE)

ler_resultado <- function(filepath) {
  fname <- basename(filepath)
  partes <- str_match(fname, "(\\w+)-setup-(\\w+)-(\\w+)-(\\w+)\\.txt")
  estrutura <- partes[2]
  setup <- partes[3]
  operacao <- partes[4]
  tipo <- partes[5]
  
  dados <- read.table(filepath, header = FALSE, col.names = c("n", "tempo"))
  
  dados <- dados %>%
    group_by(n) %>%
    summarise(tempo = quantile(tempo, 0.25), .groups = "drop")
  
  dados$estrutura <- estrutura
  dados$setup <- setup
  dados$operacao <- operacao
  dados$tipo <- tipo
  
  return(dados)
}

dados <- do.call(rbind, lapply(arquivos, ler_resultado))

operacoes <- unique(dados$operacao)
tipos <- unique(dados$tipo)
setups <- unique(dados$setup)
estruturas <- unique(dados$estrutura)

cores <- c(
  "RedBlackTree" = "red",
  "LinkedList"   = "forestgreen",
  "SkipList"     = "blue",
  "AVLTree"      = "purple"
)

nomes <- c(
  "RedBlackTree" = "Árvore rubro-negra",
  "AVLTree"      = "AVL",
  "LinkedList"   = "LinkedList",
  "SkipList"     = "SkipList"
)

dir.create(file.path(output_dir, "geral"), showWarnings = FALSE, recursive = TRUE)

for (op in operacoes) {
  for (tp in tipos) {
    for (st in setups) {
      df_sub <- dados %>% filter(operacao == op, tipo == tp, setup == st)
      titulo <- paste("Operação:", op, "| Tipo:", tp, "| Setup:", st)
      
      p <- ggplot(df_sub, aes(x = n, y = tempo, color = estrutura)) +
        geom_line(size = 1) +
        labs(title = titulo, x = "Número de entradas", y = "Tempo (ms)", color = "Estrutura") +
        scale_color_manual(values = cores, labels = nomes) + 
        theme_minimal(base_size = 14) +
        theme(
          plot.title = element_text(size = 10, hjust = 0.5) 
        )

      fname <- file.path(output_dir, "geral", paste0("plot_setup_", st, "_", op, "_", tp, ".png"))
      ggsave(fname, p, width = 1920/300, height = 1080/300, dpi = 300)
    }
  }
}

dir.create(file.path(output_dir, "individual"), showWarnings = FALSE, recursive = TRUE)

for (op in operacoes) {
  for (tp in tipos) {
    for (st in setups) {
      for (est in estruturas) {
        df_sub <- dados %>% filter(operacao == op, tipo == tp, setup == st, estrutura == est)
        titulo <- paste("Estrutura:", est, "| Operação:", op, "| Tipo:", tp, "| Setup:", st)
        
        p <- ggplot(df_sub, aes(x = n, y = tempo, color = estrutura)) +
          geom_line(size = 1) +
          labs(title = titulo, x = "Número de entradas", y = "Tempo (ms)", color = "Estrutura") +
          scale_color_manual(values = cores, labels = nomes) + 
          theme_minimal(base_size = 14) +
          theme(
            plot.title = element_text(size = 10, hjust = 0.5),
            legend.position = "none"
          )
        
        fname <- file.path(output_dir, "individual", paste0("plot_", est, "_setup_", st, "_", op, "_", tp, ".png"))
        ggsave(fname, p, width = 1920/300, height = 1080/300, dpi = 300)
      }
    }
  }
}

dir.create(file.path(output_dir, "vs_skiplist"), showWarnings = FALSE, recursive = TRUE)

for (op in operacoes) {
  for (tp in tipos) {
    for (est in estruturas) {
      if (est != "skiplist") {
        for (st in setups) {
          df_sub <- dados %>% filter(operacao == op, tipo == tp, setup == st, estrutura %in% c("skiplist", est))
          titulo <- paste("SkipList vs", est, "| Operação:", op, "| Tipo:", tp, "| Setup:", st)
          
          p <- ggplot(df_sub, aes(x = n, y = tempo, color = estrutura)) +
            geom_line(size = 1) +
            labs(title = titulo, x = "Número de entradas", y = "Tempo (ms)", color = "Estrutura") +
            scale_color_manual(values = cores, labels = nomes) + 
            theme_minimal(base_size = 14) +
            theme(
              plot.title = element_text(size = 10, hjust = 0.5)
            )
          
          fname <- file.path(output_dir, "vs_skiplist", paste0("plot_setup_", st, "_", op, "_", tp, ".png"))
          ggsave(fname, p, width = 1920/300, height = 1080/300, dpi = 300)
        }
      }
    }
  }
}

