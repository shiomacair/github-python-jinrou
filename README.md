# github-python-jinrou
人狼ゲームのデスクトップアプリ<br>
一つの端末で遊ぶことを想定しています。

## コマンド (anaconda を使う場合)
mamba create -n tk python=3.10.9 -y<br>
mamba activate tk<br>
python jinrou_tk.py

## ルール
### 基本ルール
・最初に人数を入力し、名前を一人ずつ入力します。<br>
・役職がランダムに配られるので、一人ずつ確認します。<br>
・朝パートが始まるので、自由に会議を行い、会議が終わったら一人ずつ投票を行います。<br>
・投票で選ばれた人を処刑したあと、夜パートになります。<br>
・夜パートでは、一人ずつ順番にスキルを使います。<br>
・以降は勝利条件を満たすまで、朝パートと夜パートを繰り返します。

### 役職
村人陣営、人狼陣営、妖狐陣営があります。
#### 村人陣営
村人陣営は、妖狐を倒した後に、人狼を全滅させたら勝利です。<br>
<br>
・村人<br>
特に能力はありません。<br>
<br>
・占い師<br>
ゲーム開始時に自分以外からランダムで一人を人狼か判別します。<br>
それ以降は、夜に一人を選択して、人狼か判別します。<br>
<br>
・霊能者<br>
夜に、その日に処刑された人が人狼か判別します。<br>
<br>
・狩人<br>
夜に一人を選択して、護衛します。<br>
護衛された人間は、その日に人狼に襲撃されても死ななくなります。<br>
護衛に成功した場合、そのことは人狼、狩人のどちらも把握できません。<br>
<br>
・共有者<br>
ゲーム開始時と夜に、生存している共有者が誰かわかります。<br>
<br>
・ポンコツ<br>
ゲーム開始時に占い師、霊能者、狩人からランダムで偽役職が選ばれて、自分をその役職だと思い込みます。<br>
役職を占い師、霊能者だと思い込んだ場合、それぞれの役職同様に判別を行いますが、結果は常に人狼ではないとなります。<br>
狩人だと思い込んだ場合、護衛する相手を選べますが、その相手を人狼の襲撃から守ることはできません。

#### 人狼陣営
人狼陣営は、妖狐を倒した後に、人間の数を人狼の数以下に減らせば勝利です。<br>
<br>
・人狼<br>
ゲーム開始時と夜に、生存している人狼が誰かわかります。<br>
夜に生存している人狼から一人がランダムに選ばれて、襲撃者になります。<br>
襲撃者は、人狼以外から一人を選択して、襲撃します。<br>
襲撃された人間は、基本的に次の日の朝に死亡します。<br>
<br>
・狂人<br>
人狼陣営に所属する人間です。<br>
占い師、霊能者の能力では人狼ではないという結果になります。<br>
勝敗の判定では、人間の一人として数えられます。<br>
特に能力はありません。<br>

#### 妖狐陣営
妖狐陣営は、人狼が全滅するか、人間の数が人狼の数以下になったときに、妖狐が生きていれば勝利です。<br>
<br>
・妖狐<br>
人狼に襲撃されても死亡しません。<br>
人狼に襲撃された場合、そのことは人狼、妖狐のどちらも把握できません。<br>
占い師の占い対象になった場合、次の日の朝に死亡します。<br>
その場合のアナウンスは、人狼に殺された場合と同様です。<br>
<br>
・背徳者<br>
妖狐陣営に所属している人間です。<br>
占い師、霊能者の能力では人狼ではないという結果になります。<br>
勝敗の判定では、人間の一人として数えられます。<br>
ゲーム開始時と夜に、生存している妖狐が誰かわかります。<br>
夜が終わった時点で妖狐が全滅していた場合、朝の開始時に自殺します。<br>
