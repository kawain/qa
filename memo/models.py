from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Question(models.Model):
    cat = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="カテゴリ"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="タグ")
    answer = models.CharField(max_length=255, verbose_name="答え")
    problem = models.TextField(verbose_name="質問", blank=True, null=True)

    def __str__(self):
        text = f"<{self.id}> <{self.cat}> {self.problem[:50]}"
        return text


class Note(models.Model):
    cat = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="カテゴリ"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="タグ")
    title = models.CharField(max_length=255, verbose_name="タイトル")
    content = models.TextField(verbose_name="内容", blank=True, null=True)

    def __str__(self):
        return f"<{self.id}> {self.title}"
