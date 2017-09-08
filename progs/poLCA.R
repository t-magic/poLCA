set_colnames_chars <- function(m1) {
	colnames_chars = paste0("f <- cbind(", names(m1[2]))
	for (i in 3:length(m1)) {              # for (ループ変数 in ベクトルやリスト)
	    colnames_chars = paste(colnames_chars, names(m1[i]), sep = ",")
	}
	colnames_chars = paste0(colnames_chars, ")~1")
	return(colnames_chars)
}

calc_pol <- function(file, minc, maxc, maxiter, pol.out) {
	write("", file = file)
	for (i in minc:maxc) {
		t=capture.output(temp <- poLCA(f, m1, nclass=i, maxiter=maxiter))
	    write(t, file="data/M3.txt", append = T)
		caic <- (-2 * temp$llik) + ((log(temp$N) + 1) * temp$npar) #CAIC
		Cp <- round(pchisq(temp$Chisq, temp$resid.df, lower.tail=FALSE), 6) #ｐ値
		Gp <- round(pchisq(temp$Gsq, temp$resid.df, lower.tail=FALSE), 6) #ｐ値
		pol.out[i,] <- c(temp$aic, temp$bic, caic, Cp, Gp)
		colnames(pol.out) <- c("AIC","BIC","CAIC","Chi.p","G.p")
		rownames(pol.out) <- minc:maxc
	}
	return(pol.out)
}

draw_AIC_BIC_CAIC <- function(minc, maxc) {
	matplot(minc:maxc, pol.out[,1:3], type="b", xla="classes", yla="bic", col=2:4,
		pch=c("A","B","C"),
		main="AIC、BIC、CAICの比較\n")
	legend(2, max(pol.out), legend=c("AIC","BIC","CAIC"),col=2:4,lty=c(1:3))

	# ファイルへの書き出し
	win.metafile(filename="data/AIC-BIC-CAIC.wmf")
	matplot(minc:maxc, pol.out[,1:3], type="b", xla="classes", yla="bic", col=2:4,
		pch=c("A","B","C"),
		main="AIC、BIC、CAICの比較\nデータセット“T社フリーアンサー”の場合")
	legend(2, max(pol.out), legend=c("AIC","BIC","CAIC"),col=2:4,lty=c(1:3))
	dev.off()
}