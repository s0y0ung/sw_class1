module.exports = function(app){
    app.get("/", (req, res) => (
        res.render('product.html')
    ));

    app.get("/product/index.html", (req, res) => (
        res.render('product.html')
    ));
    
    app.get("/checkout/index.html", (req, res) => (
        res.render('checkout.html')
    ));

    app.get("/price/index.html", (req, res) => (
        res.render('price.html')
    ));
}